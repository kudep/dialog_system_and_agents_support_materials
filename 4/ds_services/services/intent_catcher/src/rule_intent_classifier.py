import re
import logging
from services_api.intent_catcher import IntentCatcherResponse, PredictedIntent, Intent, Tag

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseIntentClassifierBase:
    def predict(self, text: str) -> IntentCatcherResponse:
        raise NotImplementedError("This method must be implemented in a subclass.")


class RuleBasedIntentClassifier(BaseIntentClassifierBase):
    def __init__(self, intents, tags):
        self.tags = [Tag(**tag) for tag in tags]
        self.intents = [Intent(**intent) for intent in intents]
        self.intent_name2regexp = {
            intent.name: re.compile(r"(" + r"|".join(intent.reg_phrases) + r")", re.IGNORECASE)
            for intent in self.intents
        }

    def predict(self, text: str) -> IntentCatcherResponse:
        logger.info("  Input text: %s", text)
        logger.info("  Rule-based model predicting:")
        logger.info("  %-20s | %s", "Intent", "Matched phrases")
        logger.info("  " + "-" * 50)
        predictions = []
        for intent in self.intents:
            regexp = self.intent_name2regexp[intent.name]
            matches = regexp.findall(text)
            is_match = bool(matches)
            confidence = float(is_match)
            rule_support_reference = ""
            if is_match:
                matched_phrase = matches[0]
                if isinstance(matched_phrase, tuple):
                    matched_phrase = "".join(matched_phrase)
                for phrase in intent.reg_phrases:
                    if re.search(phrase, matched_phrase, re.IGNORECASE):
                        rule_support_reference = phrase
                        break
            predicted_intent = PredictedIntent(
                name=intent.name,
                rule_confidence=confidence,
                rule_match=is_match,
                rule_support_reference=rule_support_reference,
                semantic_confidence=0.0,
                semantic_match=False,
            )
            predictions.append(predicted_intent)
            if is_match:
                logger.info("  %-20s | %s", intent.name, rule_support_reference)
        response = IntentCatcherResponse(intent_catcher_response=predictions)
        return response
