import os
from typing import AsyncIterable, List

from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser

from backend.config import Config
from backend.datastore.qdrant_doc import QdrantDoc
from backend.interfaces.ai import AIServiceInterface
from backend.interfaces.embedding import EmbeddingServiceInterface
from backend.interfaces.loader import DocsLoaderInterface
from backend.interfaces.splitter import DocumentTransformerInterface
from backend.interfaces.vector_db import VectorDBInterface
from backend.services.prompt import PromptService
from backend.utils.logger import logger
from backend.utils.prompts import Prompts


class RAGService(object):
    def __init__(
            self,
            vector_db: VectorDBInterface,
            ai_service: AIServiceInterface,
            embedding_service: EmbeddingServiceInterface,
            text_splitter: DocumentTransformerInterface,
            docs_loader: DocsLoaderInterface,
    ) -> None:
        self.vector_db = vector_db
        self.ai_service = ai_service
        self.embedding_service = embedding_service
        self.text_splitter = text_splitter
        self.docs_loader = docs_loader
        self.collection_name = ''

    def __validate_collection_name(self) -> None:
        if not self.collection_name:
            raise ValueError('Collection name is not set.')

    def set_collection_name(self, collection_name: str) -> None:
        self.collection_name = collection_name

    def get_keywords(self, text: str) -> List[str]:
        prompt = PromptService.get_prompt(
            system_message=Prompts.RAG_KEYWORDS.value,
            human_message='{text}',
        )
        result = self.ai_service.chat_completion(prompt=prompt, text=text, parser=JsonOutputParser())
        return result.get('keywords', [])  # type: ignore

    def optimize_documents(self, documents: List[QdrantDoc]) -> List[QdrantDoc]:
        optimize_documents = []
        for document in documents:
            chunks = self.text_splitter.create_documents([document.content])
            for chunk in chunks:
                embedding = self.embedding_service.get_embedding(chunk.page_content)
                optimize_documents.append(QdrantDoc(
                    title=document.title,
                    content=chunk.page_content,
                    embedding=embedding,
                    keywords=[],  # todo: optimize receiving keywords
                ))
        return optimize_documents

    def prepare_documents(self, files_paths: List[str]) -> List[QdrantDoc]:
        documents = []
        for file_path in files_paths:
            filename = os.path.basename(file_path)
            title, _ = os.path.splitext(filename)
            content = self.docs_loader.load_text(file_path)
            documents.append(QdrantDoc(title=title, content=content, embedding=None))
        return self.optimize_documents(documents)

    def create_collection(self, files_paths: List[str]) -> None:
        self.__validate_collection_name()

        docs_for_qdrant = self.prepare_documents(files_paths)
        self.vector_db.create_collection(
            collection_name=self.collection_name,
            vector_size=Config.VECTOR_SIZE,
        )
        self.vector_db.create_vectors(collection_name=self.collection_name, docs_for_qdrant=docs_for_qdrant)

    async def search_in_documents(self, question: str) -> AsyncIterable[str]:
        prompt = PromptService.get_prompt(
            system_message=Prompts.RAG_SEARCH.value,
            human_message='{question}',
        )
        query_question = self.generate_query_question(question)
        logger.info('Search in Qdrant...')
        documents = await self.get_documents(query_question)
        logger.info('Found documents.')
        context = self.format_docs(documents)
        logger.debug(f'Context: {context}')
        async for response in self.ai_service.chat_completion(
                prompt=prompt,
                context=context,
                question=question,
        ):
            yield response

    async def search_in_knowledge(self, question: str) -> AsyncIterable[str]:
        prompt = PromptService.get_prompt(
            system_message=Prompts.SEARCH.value,
            human_message='{question}',
        )
        async for response in self.ai_service.chat_completion(prompt=prompt, question=question):
            yield response

    async def get_answer(self, question: str, rag: bool = False) -> AsyncIterable[str]:
        self.__validate_collection_name()

        if rag:
            logger.info('Search in documents...')
            async for result in self.search_in_documents(question):
                yield result
        logger.info('Search in knowledge...')
        async for result in self.search_in_knowledge(question):
            yield result

    async def get_documents(self, question: AsyncIterable[str]) -> List[Document]:
        result = ''
        async for item in question:
            result += item
        return self.vector_db.search_documents(collection_name=self.collection_name, query=result)

    def generate_query_question(self, question: str):
        prompt = PromptService.get_prompt(
            system_message=Prompts.RAG_QUERY.value,
            human_message='{question}',
        )
        return self.ai_service.chat_completion(
            prompt=prompt,
            question=question,
        )

    def format_docs(self, docs: List[Document]) -> str:
        return '\n\n'.join(
            ' Doc source: '.join([doc.page_content, doc.metadata.get('title', '')])
            for doc in docs
        )
