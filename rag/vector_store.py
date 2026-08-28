import logging
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config import settings

logger = logging.getLogger(__name__)

COLLECTION_NAME = "schema_metadata"


class VectorStoreManager:
    def __init__(self, host: str = settings.QDRANT_HOST, port: int = settings.QDRANT_PORT):
        try:
            # Connect to live Qdrant instance
            self.client = QdrantClient(host=host, port=port, timeout=5)
            # Test connection
            self.client.get_collections()
        except Exception:
            logger.warning("Could not connect to standalone Qdrant server. Falling back to local in-memory Qdrant instance.")
            self.client = QdrantClient(":memory:")

        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Creates the vector collection if it does not already exist."""
        collections = [c.name for c in self.client.get_collections().collections]
        if COLLECTION_NAME not in collections:
            # FastEmbed defaults to 384 dimensions (BAAI/bge-small-en-v1.5)
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
            logger.info(f"Created Qdrant collection: '{COLLECTION_NAME}'")

    def add_documents(self, documents: List[Dict[str, Any]]):
        """
        Embeds and upserts documents into Qdrant.
        Each document requires: 'id' (int), 'text' (str), 'metadata' (dict).
        """
        texts = [doc["text"] for doc in documents]
        payloads = [
            {"text": doc["text"], **doc.get("metadata", {})}
            for doc in documents
        ]
        ids = [doc["id"] for doc in documents]

        self.client.add(
            collection_name=COLLECTION_NAME,
            documents=texts,
            metadata=payloads,
            ids=ids
        )
        logger.info(f"Upserted {len(documents)} metadata records into '{COLLECTION_NAME}'.")

    def search_context(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Performs semantic similarity search to pull relevant database metadata."""
        results = self.client.query(
            collection_name=COLLECTION_NAME,
            query_text=query,
            limit=limit
        )

        retrieved_items = []
        for point in results:
            retrieved_items.append({
                "text": point.metadata.get("text", ""),
                "metadata": point.metadata,
                "score": point.score
            })
        return retrieved_items


# Global vector store instance
vector_store = VectorStoreManager()