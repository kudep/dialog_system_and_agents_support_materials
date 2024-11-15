from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from huggingface_hub import hf_hub_download


def load_langchain_model(
    repo_id: str = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF",
    filename: str = "Meta-Llama-3.1-8B-Instruct-Q8_0.gguf",
    n_gpu_layers: int = -1,
    n_ctx: int = 8192,
    temperature=0.5,
):
    """
    Load a LangChain model from Hugging Face Hub.
    Examples:
    ```python
    load_langchain_model(repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", filename="Meta-Llama-3.1-8B-Instruct-Q8_0.gguf")
    load_langchain_model(repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", filename="Meta-Llama-3.1-8B-Instruct-f32.gguf")
    load_langchain_model(repo_id="bartowski/Hermes-3-Llama-3.1-8B-lorablated-GGUF", filename="Hermes-3-Llama-3.1-8B-lorablated-Q8_0.gguf")
    load_langchain_model(repo_id="bartowski/Meta-Llama-3.1-70B-Instruct-GGUF", filename="Meta-Llama-3.1-70B-Instruct-Q5_K_S.gguf")
    load_langchain_model(repo_id="bartowski/Meta-Llama-3.1-70B-Instruct-GGUF", filename="Meta-Llama-3.1-70B-Instruct-IQ1_M.gguf")
    """
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    cache_file = hf_hub_download(repo_id=repo_id, filename=filename)
    return LlamaCpp(
        model_path=cache_file,
        n_gpu_layers=n_gpu_layers,
        n_ctx=n_ctx,
        temperature=temperature,
        callback_manager=callback_manager,
    )
