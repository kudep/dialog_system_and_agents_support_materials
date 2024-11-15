from typing import Any, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

from langchain_community.chat_models import GigaChat

from services_api import gigachat


CACHE = {}


class GigaChatAPI(LLM):
    model: GigaChat
    """The number of characters from the last message of the prompt to be echoed."""

    def _call(
        self,
        prompt: str,
        stop: Optional[list[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if prompt not in CACHE:
            request = gigachat.GigachatRequest.parse_raw(prompt)
            response = self.model.invoke(request.text, config={"configurable": {"temperature": 0, "max_tokens": 512}})
            response = gigachat.GigachatResponse(
                text=response.content, stop_reason=response.response_metadata["finish_reason"]
            )
            CACHE[prompt] = response.json()
        return CACHE[prompt]

    @property
    def _identifying_params(self) -> dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {"model_name": "gigachat"}

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "gigachat"
