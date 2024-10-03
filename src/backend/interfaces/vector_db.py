from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document

from backend.datastore.qdrant_doc import QdrantDoc


class VectorDBInterface(ABC):
    @abstractmethod
    def create_vectors(self, collection_name: str, docs_for_qdrant: List[QdrantDoc]) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_collection(self, collection_name: str, vector_size: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def search_documents(self, collection_name: str, query: str, limit: int = 5) -> List[Document]:
        raise NotImplementedError
