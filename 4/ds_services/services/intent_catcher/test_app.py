import pytest
from tests.data import test_cases

from services_api import intent_catcher


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    response: intent_catcher.IntentCatcherResponse = intent_catcher.chain.invoke(test_case.request.json())
    assert test_case.response_comparator(response, test_case.response)
