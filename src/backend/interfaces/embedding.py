from abc import ABC, abstractmethod
from typing import List

from langchain_core.embeddings import Embeddings


class EmbeddingServiceInterface(ABC):
    VECTOR_SIZE: int
    model: Embeddings

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        raise NotImplementedError
