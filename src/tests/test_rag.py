from unittest import mock

import pytest
from langchain_core.documents import Document

from backend.config import Config
from backend.datastore.qdrant_doc import QdrantDoc
from backend.services.rag import RAGService


@pytest.fixture
def rag_service():
    vector_db_mock = mock.MagicMock()
    ai_service_mock = mock.MagicMock()
    embedding_service_mock = mock.MagicMock()
    text_splitter_mock = mock.MagicMock()
    docs_loader_mock = mock.MagicMock()

    rag_service = RAGService(
        vector_db=vector_db_mock,
        ai_service=ai_service_mock,
        embedding_service=embedding_service_mock,
        text_splitter=text_splitter_mock,
        docs_loader=docs_loader_mock
    )
    rag_service.set_collection_name('test_collection')
    return rag_service


def test_prepare_documents(rag_service):
    filepath_mock = '/test/filepath'
    text_content_mock = 'This is a sample text content.'
    embedding_mock = [0.1, 0.2, 0.3]
    rag_service.docs_loader.load_text.return_value = text_content_mock
    rag_service.text_splitter.create_documents.return_value = [Document(page_content=text_content_mock)]
    rag_service.embedding_service.get_embedding.return_value = embedding_mock

    input_data = [filepath_mock]
    result = rag_service.prepare_documents(input_data)

    expected_result = [QdrantDoc(title='filepath', content=text_content_mock, embedding=embedding_mock)]
    rag_service.docs_loader.load_text.assert_called_once_with(filepath_mock)
    rag_service.text_splitter.create_documents.assert_called_once_with([text_content_mock])
    rag_service.embedding_service.get_embedding.assert_called_once_with(text_content_mock)

    assert result[0].title == expected_result[0].title
    assert result[0].content == expected_result[0].content
    assert result[0].embedding == expected_result[0].embedding


def test_create_collection(rag_service):
    filepath_mock = '/test/filepath'
    input_data = [filepath_mock]
    rag_service.create_collection(input_data)

    rag_service.vector_db.create_collection.assert_called_once_with(
        collection_name=rag_service.collection_name,
        vector_size=Config.VECTOR_SIZE,
    )
    rag_service.vector_db.create_vectors.assert_called_once()


@pytest.mark.asyncio
async def test_search_in_documents(rag_service):
    question_mock = 'What is lorem ipsum?'
    async for _ in rag_service.get_answer(question_mock, rag=True):
        pass

    rag_service.ai_service.chat_completion.assert_called()


@pytest.mark.asyncio
async def test_search_in_knowledge(rag_service):
    question_mock = 'What is lorem ipsum?'
    async for _ in rag_service.get_answer(question_mock, rag=False):
        pass

    rag_service.ai_service.chat_completion.assert_called()


@pytest.mark.asyncio
async def test_get_answer(rag_service):
    question_mock = 'What is lorem ipsum?'
    async for _ in rag_service.get_answer(question_mock, rag=True):
        pass

    rag_service.ai_service.chat_completion.assert_called()
    rag_service.ai_service.chat_completion.reset_mock()

    async for _ in rag_service.get_answer(question_mock, rag=False):
        pass
    rag_service.ai_service.chat_completion.assert_called()
