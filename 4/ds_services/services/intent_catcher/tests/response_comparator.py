from services_api.intent_catcher import IntentCatcherResponse


def check_response(checked_response: IntentCatcherResponse, target_response: list) -> bool:
    detected_intents = list(checked_response.detected_intents())
    print(f"target_response: {target_response},\n detected intents: {detected_intents}")
    return detected_intents[:1] == target_response


def check_support_reference(checked_response: IntentCatcherResponse, target_data: list) -> bool:
    if not checked_response.intent_catcher_response:
        return False

    first_intent = checked_response.intent_catcher_response[:1][0]
    reference_type = target_data[0].get("type")
    target_phrase = target_data[0].get("phrase")

    if reference_type == "rule":
        return [first_intent.rule_support_reference] == [target_phrase]
    elif reference_type == "semantic":
        return [first_intent.semantic_support_reference] == [target_phrase]
    return False


def check_intent_scope(checked_response: IntentCatcherResponse, target_scope: list) -> bool:
    return [intent.scope for intent in checked_response.intent_catcher_response[:1]] == target_scope


def check_multilabel_classification(checked_response: IntentCatcherResponse, target_intents: list) -> bool:
    detected_intents = {intent.name for intent in checked_response.intent_catcher_response if intent.semantic_match}
    return detected_intents == set(target_intents)
