from pydantic import BaseModel


class LLMOutput(BaseModel):
    text: str


def match_response(response: str, response_candidates: list[str]) -> bool:
    return any(response in resp for resp in response_candidates)
