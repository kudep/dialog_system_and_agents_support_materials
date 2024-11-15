import pytest

from services_api import gigachat
from tests.data import test_cases


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    response = gigachat.chain.invoke(test_case.request.json())
    if response.stop_reason == "blacklist":
        assert response.stop_reason == test_case.response.stop_reason
    else:
        assert response.stop_reason == test_case.response.stop_reason and response.text == test_case.response.text
