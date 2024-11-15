from fastapi import FastAPI
from langserve import add_routes
from pydantic_settings import BaseSettings

from src.utils import load_langchain_model


class Settings(BaseSettings, case_sensitive=True):
    REPO_ID: str = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
    FILENAME: str = "Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"
    N_GPU_LAYERS: int = -1
    N_CTX: int = 8192
    TEMPERATURE: float = 0.6


settings = Settings()

app = FastAPI()

model = load_langchain_model(
    repo_id=settings.REPO_ID,
    filename=settings.FILENAME,
    n_gpu_layers=settings.N_GPU_LAYERS,
    n_ctx=settings.N_CTX,
    temperature=settings.TEMPERATURE,
)

add_routes(app, model)
