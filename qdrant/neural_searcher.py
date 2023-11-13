from typing import List
from qdrant_client import QdrantClient
from qdrant.config import QDRANT_URL, QDRANT_API_KEY, EMBEDDINGS_MODEL
from sentence_transformers import SentenceTransformer


class NeuralSearcher:

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, prefer_grpc=True)
        # self.qdrant_client.set_model(EMBEDDINGS_MODEL)
        self.encoder = SentenceTransformer(EMBEDDINGS_MODEL)

    def query(self, text: str, limit=5) -> List:
        hits = self.qdrant_client.query(
            collection_name=self.collection_name,
            query_text=text,
            limit=limit
        )
        return hits

    def search(self, text: str, limit=5) -> List:
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=self.encoder.encode(text).tolist(),
            limit=limit
        )
        return hits
