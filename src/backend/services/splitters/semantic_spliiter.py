from typing import List

from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker

from backend.interfaces.embedding import EmbeddingServiceInterface
from backend.interfaces.splitter import DocumentTransformerInterface


class SemanticTextSplitter(DocumentTransformerInterface):
    def __init__(self, embeddings: EmbeddingServiceInterface):
        self.splitter = SemanticChunker(embeddings.model, breakpoint_threshold_type='standard_deviation')

    def create_documents(self, texts: List[str]) -> List[Document]:
        return self.splitter.create_documents(texts)
