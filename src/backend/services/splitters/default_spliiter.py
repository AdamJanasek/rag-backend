from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.interfaces.splitter import DocumentTransformerInterface


class DefaultTextSplitter(DocumentTransformerInterface):
    def __init__(self, chunk_size: int = 1000):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_size * 0.1,  # 10% overlap
            length_function=len,
            is_separator_regex=False,
        )

    def create_documents(self, texts: List[str]) -> List[Document]:
        return self.splitter.create_documents(texts)
