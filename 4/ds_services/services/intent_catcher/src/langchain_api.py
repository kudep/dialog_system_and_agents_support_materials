from collections import defaultdict
from typing import Any, Optional, List, Dict, Tuple
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from services_api.intent_catcher import IntentCatcherResponse, PredictedIntent, Intent, IntentCatcherRequest
from .rule_intent_classifier import RuleBasedIntentClassifier
from .bge_intent_classifier import BGEIntentClassifier
from pydantic import Field


class IntentClassifierAPI(LLM):
    rule_based_model: RuleBasedIntentClassifier = Field(...)
    bge_model: BGEIntentClassifier = Field(...)
    threshold: float = Field(default=0.5)
    intent_scopes: Dict[str, str] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        rule_based_model: RuleBasedIntentClassifier,
        bge_model: BGEIntentClassifier,
        threshold: float = 0.6761,
        intent_scopes: Dict[str, str] = None,
        **kwargs,
    ):
        super().__init__(rule_based_model=rule_based_model, bge_model=bge_model, threshold=threshold, **kwargs)
        self.intent_scopes = intent_scopes or {}

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        request: IntentCatcherRequest = IntentCatcherRequest.parse_raw(prompt)
        result = self._classify_intent(request.intent_catcher_request)
        return IntentCatcherResponse(intent_catcher_response=result).json()

    def _classify_intent(self, prompt: str) -> List[PredictedIntent]:
        rule_based_results = self.rule_based_model.predict(prompt)
        bge_results = self.bge_model.predict(prompt, threshold=self.threshold)

        combined_results = []
        tag_groups: Dict[str, List[Tuple[PredictedIntent, Intent]]] = defaultdict(list)

        for intent in set(r.name for r in rule_based_results.intent_catcher_response) | set(r[0] for r in bge_results):
            rule_match = next((r for r in rule_based_results.intent_catcher_response if r.name == intent), None)
            semantic_match = next((r for r in bge_results if r[0] == intent), None)
            intent_info = next((i for i in self.rule_based_model.intents if i.name == intent), None)

            predicted_intent = PredictedIntent(
                name=intent,
                scope=self.intent_scopes.get(intent, ""),
                rule_confidence=rule_match.rule_confidence if rule_match else 0.0,
                rule_match=rule_match.rule_match if rule_match else False,
                rule_support_reference=rule_match.rule_support_reference if rule_match else "",
                semantic_confidence=semantic_match[1] if semantic_match else 0.0,
                semantic_match=semantic_match[3] if semantic_match else False,
                semantic_support_reference=semantic_match[2] if semantic_match else "",
            )

            if intent_info and intent_info.tags:
                for tag in intent_info.tags:
                    tag_groups[tag].append((predicted_intent, intent_info))
            else:
                combined_results.append(predicted_intent)

        for tag, intents in tag_groups.items():
            tag_info = next((t for t in self.rule_based_model.tags if t.name == tag), None)
            if tag_info and tag_info.selection_mode == "best" and len(intents) > 1:
                best_intent = max(intents, key=lambda x: max(x[0].rule_confidence, x[0].semantic_confidence))
                for intent, _ in intents:
                    if intent != best_intent[0]:
                        intent.semantic_match = False
            combined_results.extend([intent for intent, _ in intents])

        return sorted(combined_results, key=lambda x: x.semantic_confidence, reverse=True)

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model_name": "combined-intent-classifier"}

    @property
    def _llm_type(self) -> str:
        return "multi-model-intent-classifier"
