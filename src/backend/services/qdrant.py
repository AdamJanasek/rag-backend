import time
from typing import List

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from backend.datastore.qdrant_doc import QdrantDoc
from backend.interfaces.embedding import EmbeddingServiceInterface
from backend.interfaces.vector_db import VectorDBInterface
from backend.utils.logger import logger


class QdrantService(VectorDBInterface):
    FETCH_K_MULTIPLIER = 2

    def __init__(self, host: str, port: int, embedding_service: EmbeddingServiceInterface) -> None:
        self.client = QdrantClient(host=host, port=port)
        self.embedding_service = embedding_service

    def create_vectors(self, collection_name: str, docs_for_qdrant: List[QdrantDoc]) -> None:
        points = [
            PointStruct(
                id=doc_id,
                payload=doc.as_payload(),
                vector=doc.embedding,  # type: ignore
            )
            for doc_id, doc in enumerate(docs_for_qdrant)
        ]
        self.client.upsert(collection_name=collection_name, points=points)

    def create_collection(self, collection_name: str, vector_size: int) -> None:
        vectors_config = VectorParams(distance=Distance.COSINE, size=vector_size)
        self.client.recreate_collection(collection_name=collection_name, vectors_config=vectors_config)

    def search_documents(
            self,
            collection_name: str,
            query: str,
            limit: int = 5,
    ) -> list[Document]:
        qdrant = Qdrant(
            client=self.client,
            collection_name=collection_name,
            embeddings=self.embedding_service.model,
        )
        logger.info('Retrieve documents...')
        start_time = time.time()
        documents = qdrant.max_marginal_relevance_search(
            query,
            k=limit,
            fetch_k=self.FETCH_K_MULTIPLIER * limit,  # fetch more to get better results
        )
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f'Documents received in {duration:.2f} seconds.')
        return documents
