import pathlib
from fastapi import FastAPI
from langserve import add_routes
from src.rule_intent_classifier import RuleBasedIntentClassifier
from src.bge_intent_classifier import BGEIntentClassifier
from src.langchain_api import IntentClassifierAPI
from src.data_preparation import update_dataset_if_needed, load_all_intents_and_tags
from src.vector_store import FaissVectorStore

app = FastAPI()

dataset_dir = pathlib.Path("/app/dataset")
data_dir = pathlib.Path("/data")
phrases_csv_file = data_dir / "intent_phrases.csv"
vector_store_dir = data_dir / "vector_store"

intents, tags, intent_scopes = load_all_intents_and_tags(dataset_dir)
dataset_updated = update_dataset_if_needed(dataset_dir, phrases_csv_file)

rule_based_model = RuleBasedIntentClassifier(intents=intents, tags=tags)
vector_store = FaissVectorStore(dimension=1024)
bge_model = BGEIntentClassifier(
    vector_store=vector_store,
    phrases_csv_file=phrases_csv_file,
    dataset_dir=dataset_dir,
    vector_store_dir=vector_store_dir,
)

bge_model.update_vector_store_if_needed()

classifier_api = IntentClassifierAPI(
    rule_based_model=rule_based_model, bge_model=bge_model, threshold=0.6761, intent_scopes=intent_scopes
)

add_routes(app, classifier_api)
