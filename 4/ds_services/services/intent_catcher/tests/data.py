from pydantic.v1 import BaseModel
from . import response_comparator
from services_api.intent_catcher import IntentCatcherRequest


class TestCase(BaseModel):
    name: str
    request: IntentCatcherRequest
    response: list
    response_comparator: object = response_comparator.check_response


test_cases = [
    TestCase(
        name="multilabel_classification_test",
        request=IntentCatcherRequest(intent_catcher_request="Как мне оформить возврат товара?"),
        response=["query_return_item", "order_is_not_accepted"],
        response_comparator=response_comparator.check_multilabel_classification,
    ),
    TestCase(
        name="rule_support_reference_test",
        request=IntentCatcherRequest(intent_catcher_request="иди на расстояние"),
        response=[
            {
                "type": "rule",
                "phrase": r"(?i)(?:пожалуйста,?\s*)?(?:робот,?\s*)?(?:иди(?:те)?|прой(?:ди("
                r"?:те)?|ти)|продвин(?:ь(?:ся|тесь)|уться)|перемести("
                r"?:сь|тесь)|двигай(?:ся|тесь)|шевели(?:сь|тесь)|сдвинь(?:ся|тесь)|("
                r"?:с)?дела(?:й(?:те)?|ть)\s+(?:шаг|движение))(?:\s+(?:на\s+("
                r"?:расстояние|дистанцию))?\s+(?:\d+|[а-я]+)?\s*(?:метр("
                r"?:ов|а)?|шаг(?:ов|а)?|единиц(?:ы)?|м\.?|см\.?)?)?(?:\s+("
                r"?:вперед|назад|вправо|влево|в\s+сторону|к|от|в\s+направлении))?",
            }
        ],
        response_comparator=response_comparator.check_support_reference,
    ),
    TestCase(
        name="semantic_support_reference_test",
        request=IntentCatcherRequest(intent_catcher_request="подними этот стул, пожалуйста"),
        response=[{"type": "semantic", "phrase": "пожалуйста, подними этот стул"}],
        response_comparator=response_comparator.check_support_reference,
    ),
    TestCase(
        name="scope autopilot",
        request=IntentCatcherRequest(intent_catcher_request="иди на расстояние"),
        response=["direct_commands"],
        response_comparator=response_comparator.check_intent_scope,
    ),
    TestCase(
        name="scope ordering",
        request=IntentCatcherRequest(intent_catcher_request="У меня есть вопрос"),
        response=["ordering_intents"],
        response_comparator=response_comparator.check_intent_scope,
    ),
    TestCase(
        name="cmd move_forward",
        request=IntentCatcherRequest(intent_catcher_request="пожалуйста, проедь вперед на 20 метров"),
        response=["move_forward"],
    ),
    TestCase(
        name="cmd move_backward",
        request=IntentCatcherRequest(intent_catcher_request="тебе стоит отъехать назад 5 метров"),
        response=["move_backward"],
    ),
    TestCase(
        name="cmd GO",
        request=IntentCatcherRequest(intent_catcher_request="иди на расстояние"),
        response=["GO"],
    ),
    TestCase(
        name="cmd pick_up",
        request=IntentCatcherRequest(intent_catcher_request="подними этот стул, пожалуйста"),
        response=["pick_up"],
    ),
    TestCase(
        name="cmd place",
        request=IntentCatcherRequest(intent_catcher_request="поставь эту коробку в угол"),
        response=["place"],
    ),
    TestCase(
        name="cmd say",
        request=IntentCatcherRequest(intent_catcher_request="повтори за мной, пожалуйста"),
        response=["say"],
    ),
    TestCase(
        name="cmd sit_down",
        request=IntentCatcherRequest(intent_catcher_request="можешь сесть рядом"),
        response=["sit_down"],
    ),
    TestCase(
        name="cmd stand_up",
        request=IntentCatcherRequest(intent_catcher_request="встань, пожалуйста"),
        response=["stand_up"],
    ),
    TestCase(
        name="cmd stop",
        request=IntentCatcherRequest(intent_catcher_request="прекрати шуметь"),
        response=["stop"],
    ),
    TestCase(
        name="cmd turn_right",
        request=IntentCatcherRequest(intent_catcher_request="можешь завернуть направо"),
        response=["turn_right"],
    ),
    TestCase(
        name="cmd turn_left",
        request=IntentCatcherRequest(intent_catcher_request="можешь завернуть налево"),
        response=["turn_left"],
    ),
    TestCase(
        name="cmd status",
        request=IntentCatcherRequest(intent_catcher_request="сообщи статус"),
        response=["status"],
    ),
    TestCase(
        name="cmd enable_autopilot",
        request=IntentCatcherRequest(intent_catcher_request="автопилот включи"),
        response=["enable_autopilot"],
    ),
    TestCase(
        name="cmd disable_autopilot",
        request=IntentCatcherRequest(intent_catcher_request="отключи автопилот"),
        response=["disable_autopilot"],
    ),
    TestCase(
        name="cmd world_state",
        request=IntentCatcherRequest(intent_catcher_request="сообщи ситуацию в мире"),
        response=["world_state"],
    ),
    TestCase(
        name="cmd drop",
        request=IntentCatcherRequest(intent_catcher_request="брось это здесь"),
        response=["drop"],
    ),
    TestCase(
        name="cmd set_point",
        request=IntentCatcherRequest(intent_catcher_request="отметь точку, пожалуйста"),
        response=["set_point"],
    ),
    TestCase(
        name="get_order",
        request=IntentCatcherRequest(intent_catcher_request="Хочу забрать свой заказ"),
        response=["get_order"],
    ),
    TestCase(
        name="about_pickup_point",
        request=IntentCatcherRequest(intent_catcher_request="Расскажите о режиме работы ПВЗ"),
        response=["about_pickup_point"],
    ),
    TestCase(
        name="off_topic",
        request=IntentCatcherRequest(intent_catcher_request="У меня есть вопрос"),
        response=["off_topic"],
    ),
    TestCase(
        name="order_is_accepted",
        request=IntentCatcherRequest(intent_catcher_request="Да, все подходит, я забираю заказ"),
        response=["order_is_accepted"],
    ),
    TestCase(
        name="order_is_not_accepted",
        request=IntentCatcherRequest(intent_catcher_request="Нет, не подходит, оформлю возврат"),
        response=["order_is_not_accepted"],
    ),
    TestCase(
        name="have_more_questions",
        request=IntentCatcherRequest(intent_catcher_request="Да, у меня есть еще вопрос"),
        response=["have_more_questions"],
    ),
    TestCase(
        name="have_no_more_questions",
        request=IntentCatcherRequest(intent_catcher_request="Нет, вопросов больше нет, спасибо"),
        response=["have_no_more_questions"],
    ),
    TestCase(
        name="ready_to_get_order",
        request=IntentCatcherRequest(intent_catcher_request="Хочу получить заказ"),
        response=["ready_to_get_order"],
    ),
    TestCase(
        name="not_ready_to_get_order",
        request=IntentCatcherRequest(intent_catcher_request="Нет, я пока не хочу забирать заказ"),
        response=["not_ready_to_get_order"],
    ),
    TestCase(
        name="query_working_hours",
        request=IntentCatcherRequest(intent_catcher_request="Какой у вас график работы?"),
        response=["query_working_hours"],
    ),
    TestCase(
        name="query_order_conditions",
        request=IntentCatcherRequest(intent_catcher_request="Какие условия выдачи заказов"),
        response=["query_order_conditions"],
    ),
    TestCase(
        name="query_delay_order",
        request=IntentCatcherRequest(intent_catcher_request="Можно ли отложить получение заказа?"),
        response=["query_delay_order"],
    ),
    TestCase(
        name="query_return_item",
        request=IntentCatcherRequest(intent_catcher_request="Как мне оформить возврат товара?"),
        response=["query_return_item"],
    ),
    # extended cmd intents
    TestCase(
        name="tesla:windshield_wipers_full_match",
        request=IntentCatcherRequest(intent_catcher_request="включить дворники"),
        response=["windshield_wipers"],
    ),
    TestCase(
        name="tesla:windshield_wipers_partial_match",
        request=IntentCatcherRequest(intent_catcher_request=" Включить дворники, "),
        response=["windshield_wipers"],
    ),
    TestCase(
        name="tesla:mirror_fold",
        request=IntentCatcherRequest(intent_catcher_request="Сложи зеркала"),
        response=["mirror_fold"],
    ),
    TestCase(
        name="tesla:lock_doors",
        request=IntentCatcherRequest(intent_catcher_request="Заблокируй двери"),
        response=["lock_doors"],
    ),
    TestCase(
        name="tesla:set_temperature",
        request=IntentCatcherRequest(intent_catcher_request="Установи температуру на..."),
        response=["set_temperature"],
    ),
    TestCase(
        name="tesla:ac_on",
        request=IntentCatcherRequest(intent_catcher_request="Включи кондиционер"),
        response=["ac_on"],
    ),
    TestCase(
        name="tesla:call_contact",
        request=IntentCatcherRequest(intent_catcher_request="Позвони Васе"),
        response=["call_contact"],
    ),
    TestCase(
        name="tesla:play_media",
        request=IntentCatcherRequest(intent_catcher_request="Воспроизведи музыку"),
        response=["play_media"],
    ),
    TestCase(
        name="unitree_go:dance",
        request=IntentCatcherRequest(intent_catcher_request="Танцуй"),
        response=["dance"],
    ),
    TestCase(
        name="unitree_go:jump_turn",
        request=IntentCatcherRequest(intent_catcher_request="Прыжок с поворотом"),
        response=["jump_turn"],
    ),
    TestCase(
        name="unitree_go:tilt",
        request=IntentCatcherRequest(intent_catcher_request="Наклонись назад"),
        response=["tilt"],
    ),
    TestCase(
        name="unitree_go:follow",
        request=IntentCatcherRequest(intent_catcher_request="Следуй за мной"),
        response=["follow"],
    ),
    TestCase(
        name="unitree_go:search_view",
        request=IntentCatcherRequest(intent_catcher_request="Найди стул"),
        response=["search_view"],
    ),
    TestCase(
        name="unitree_go:describe_view",
        request=IntentCatcherRequest(intent_catcher_request="Опиши объект перед тобой"),
        response=["describe_view"],
    ),
    TestCase(
        name="unitree_go:search_data_base",
        request=IntentCatcherRequest(intent_catcher_request="Обнови последний объект"),
        response=["search_data_base"],
    ),
    TestCase(
        name="unitree_go:question_view",
        request=IntentCatcherRequest(intent_catcher_request="Что перед тобой?"),
        response=["question_view"],
    ),
    TestCase(
        name="unitree_go:go_user",
        request=IntentCatcherRequest(intent_catcher_request="Подойди ко мне"),
        response=["go_user"],
    ),
    #################################################################################################################
    #################################################################################################################
    #################################################################################################################
    # TestCase(
    #     name="cmd go_to",
    #     request=IntentCatcherRequest(intent_catcher_request="иди к точке на карте"),
    #     response=["go_to"],
    # ),
    # TestCase(
    #     name="cmd random_phrases",
    #     request=IntentCatcherRequest(intent_catcher_request="поговорим о погоде"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-1",
    #     request=IntentCatcherRequest(intent_catcher_request="Иди вперед и возьми книгу"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-2",
    #     request=IntentCatcherRequest(intent_catcher_request="Двигайся назад и положи это"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-3",
    #     request=IntentCatcherRequest(intent_catcher_request="Остановись и скажи, что ты видишь"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-4",
    #     request=IntentCatcherRequest(intent_catcher_request="Повернись направо и иди вперед"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-5",
    #     request=IntentCatcherRequest(intent_catcher_request="Сядь и расскажи о своем состоянии"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-6",
    #     request=IntentCatcherRequest(intent_catcher_request="Встань и иди назад"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-7",
    #     request=IntentCatcherRequest(intent_catcher_request="Отключи автопилот и остановись"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-8",
    #     request=IntentCatcherRequest(intent_catcher_request="Подними это и положи туда"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-9",
    #     request=IntentCatcherRequest(intent_catcher_request="Двигайся вперед и влево"),
    #     response=["random_phrases"],
    # ),
    # TestCase(
    #     name="cmd multi-label-10",
    #     request=IntentCatcherRequest(intent_catcher_request="Скажи, где ты находишься, и иди вперед"),
    #     response=["random_phrases"],
    # ),
]

test_cases = {test_case.name: test_case for test_case in test_cases}
