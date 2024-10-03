from abc import ABC, abstractmethod


class DocsLoaderInterface(ABC):
    @abstractmethod
    def load_text(self, doc_path: str) -> str:
        raise NotImplementedError
