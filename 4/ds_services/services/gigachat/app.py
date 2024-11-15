from fastapi import FastAPI
from langserve import add_routes
from langchain_community.chat_models import GigaChat

from src.langchain_api import GigaChatAPI

app = FastAPI()

model = GigaChat(verify_ssl_certs=False, scope="GIGACHAT_API_CORP")

add_routes(app, GigaChatAPI(model=model))
