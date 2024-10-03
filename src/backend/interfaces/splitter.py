from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class DocumentTransformerInterface(ABC):
    @abstractmethod
    def create_documents(self, texts: List[str]) -> List[Document]:
        raise NotImplementedError
