import pytest

from services_api.remote import ExtendedRemoteRunnable
from tests.data import test_cases

URL = "http://localhost:8000"


@pytest.mark.parametrize("test_case", test_cases.values(), ids=test_cases.keys())
def test(test_case):
    chain = ExtendedRemoteRunnable(URL, stop=test_case.stop)
    response_candidates = []
    for _ in range(test_case.repeat_times):
        response_candidates.append(chain.invoke(test_case.request))
    assert test_case.response_comparator(test_case.response, response_candidates)
