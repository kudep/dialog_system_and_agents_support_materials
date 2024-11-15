import faiss
import logging
import numpy as np

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class FaissVectorStore:
    def __init__(self, dimension, nprobe=1):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.ntotal = 0
        self.nprobe = nprobe

    def add(self, vectors):
        logger.info(f"Adding {len(vectors)} vectors to FAISS index")
        normalized_vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]
        self.index.add(normalized_vectors.astype("float32"))
        self.ntotal += len(vectors)

    def search(self, query_vector, k=-1):
        if k == -1:
            k = self.ntotal

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        if query_vector.shape[1] != self.dimension:
            logger.error(
                f"Query vector dimension {query_vector.shape[1]} does not match index dimension {self.dimension}"
            )
            return np.array([]), np.array([])

        try:
            normalized_query = query_vector / np.linalg.norm(query_vector)
            similarities, indices = self.index.search(normalized_query.astype("float32"), k)
            return similarities.flatten(), indices.flatten()
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return np.array([]), np.array([])
