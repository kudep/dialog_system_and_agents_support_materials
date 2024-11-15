import logging
import pandas as pd
import numpy as np
import torch
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
from .data_preparation import get_dir_hash
import re

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class BGEIntentClassifier:
    def __init__(
        self,
        vector_store,
        model_name="deepvk/USER-bge-m3",
        phrases_csv_file="/data/intent_phrases.csv",
        dataset_dir="/app/dataset",
        vector_store_dir="/data/vector_store",
        device=None,
    ):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": device})
        self.phrases_csv_file = Path(phrases_csv_file)
        self.dataset_dir = Path(dataset_dir)
        self.vector_store_dir = Path(vector_store_dir)
        self.current_dir_hash = get_dir_hash(self.dataset_dir)
        self.vectors_phrases_csv_file = self._get_vectors_phrases_csv_file()
        self.vector_store = vector_store
        if self.vectors_phrases_csv_file.exists():
            logger.info(f"Loading existing vectors from {self.vectors_phrases_csv_file}")
            self.df = pd.read_pickle(self.vectors_phrases_csv_file)
        else:
            logger.info("Vector file not found. It will be created when needed.")
            self.df = pd.read_csv(self.phrases_csv_file)

        self.intents = self.df["intent"].unique()

    def _get_vectors_phrases_csv_file(self):
        return self.vector_store_dir / f"intent_phrases_with_vectors_{self.current_dir_hash}.pkl"

    def _batch_embed(self, phrases, batch_size=32):
        vectors = []
        for i in tqdm(range(0, len(phrases), batch_size), desc="Embedding phrases"):
            batch = phrases[i : i + batch_size]
            batch_vectors = self.embeddings.embed_documents(batch)
            vectors.extend(batch_vectors)
        return vectors

    def save_vectors(self):
        self.vector_store_dir.mkdir(parents=True, exist_ok=True)
        self.df.to_pickle(self.vectors_phrases_csv_file)
        logger.info(f"Vectors saved to {self.vectors_phrases_csv_file}")

    def predict(self, phrase: str, threshold: float = 0.6761, k: int = 33) -> list:
        logger.info("   BGE model predicting:")
        logger.info("   %-20s | %-10s | %s", "Intent", "Confidence", "Example")
        logger.info("   " + "-" * 70)

        input_vector = np.array(self.embeddings.embed_documents([phrase])[0]).reshape(1, -1)
        similarities, indices = self.vector_store.search(input_vector, k=k)

        intent_scores = {intent: 0.0 for intent in self.intents}
        intent_examples = {intent: "" for intent in self.intents}

        for similarity, idx in zip(similarities, indices):
            intent = self.df.iloc[int(idx)]["intent"]
            if similarity > intent_scores[intent]:
                intent_scores[intent] = float(similarity)
                intent_examples[intent] = self.df.iloc[int(idx)]["phrase"]

        results = [
            (intent, score, intent_examples[intent], score >= threshold) for intent, score in intent_scores.items()
        ]

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        for intent, score, example, above_threshold in sorted_results:
            if above_threshold:
                logger.info("   %-20s | %-10.4f | '%s'", intent, score, example)
            else:
                logger.debug("   %-20s | %-10.4f | (below threshold)", intent, score)

        return sorted_results

    def update_vector_store_if_needed(self):
        current_dir_hash = get_dir_hash(self.dataset_dir)

        existing_vector_files = list(self.vector_store_dir.glob("intent_phrases_with_vectors_*.pkl"))

        if not existing_vector_files:
            logger.info("No existing vector store found. Creating new one.")
            self.current_dir_hash = current_dir_hash
            self.vectors_phrases_csv_file = self._get_vectors_phrases_csv_file()
            self.df = pd.read_csv(self.phrases_csv_file)
            self.df["vector"] = self._batch_embed(self.df["phrase"].tolist())
            self.save_vectors()
            logger.info("Vector store created.")
        else:
            existing_file = existing_vector_files[0]
            existing_hash = re.search(r"intent_phrases_with_vectors_(.+)\.pkl", existing_file.name)

            if existing_hash and existing_hash.group(1) != current_dir_hash:
                logger.info("Intents directory has changed. Updating vector store.")

                for old_file in existing_vector_files:
                    old_file.unlink()
                    logger.info(f"Deleted old vector store: {old_file}")

                self.current_dir_hash = current_dir_hash
                self.vectors_phrases_csv_file = self._get_vectors_phrases_csv_file()
                self.df = pd.read_csv(self.phrases_csv_file)
                self.df["vector"] = self._batch_embed(self.df["phrase"].tolist())
                self.save_vectors()
                logger.info("Vector store updated.")
            else:
                logger.info("Vector store is up to date.")
                self.vectors_phrases_csv_file = existing_file
                self.current_dir_hash = current_dir_hash
        vectors = np.stack(self.df["vector"].values)
        self.vector_store.add(vectors)
        self.intents = self.df["intent"].unique()
