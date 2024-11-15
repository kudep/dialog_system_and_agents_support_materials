from pydantic import BaseModel
from . import response_comparators, prompts


class TestCase(BaseModel):
    name: str
    request: str
    stop: list[str] = ['"', "\n"]
    repeat_times: int = 3
    response: str
    response_comparator: object = response_comparators.match_response


test_cases = [
    TestCase(name="Slot Extracting", request=prompts.place_slot_extractor_prompt, response="к этому корпусу"),
]

test_cases = {test_case.name: test_case for test_case in test_cases}
