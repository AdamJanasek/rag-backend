import json
import os

import sentry_sdk
from dotenv import load_dotenv
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import ResponseStream
from sanic_cors import CORS

from backend.config import Config
from backend.datastore.chat_payload import ChatPayload
from backend.datastore.save_payload import SavePayload
from backend.services.azure_ai import AzureAIService
from backend.services.azure_embeddings import AzureEmbeddingService
from backend.services.docs_loader import DocsLoader
from backend.services.qdrant import QdrantService
from backend.services.rag import RAGService
from backend.services.splitters.default_spliiter import DefaultTextSplitter
from backend.utils.helpers import save_file, validate_files

sentry_sdk.init(
    dsn=Config.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app = Sanic('RAG')
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

load_dotenv()

ai_service = AzureAIService(
    deployment_name=Config.CHAT_DEPLOYMENT_NAME,
)
embedding_service = AzureEmbeddingService(
    deployment_name=Config.EMBEDDING_DEPLOYMENT_NAME,
)
text_splitter = DefaultTextSplitter()
qdrant_service = QdrantService(
    host=Config.QDRANT_HOST,
    port=Config.QDRANT_PORT,
    embedding_service=embedding_service,
)

rag_service = RAGService(
    vector_db=qdrant_service,
    ai_service=ai_service,
    embedding_service=embedding_service,
    text_splitter=text_splitter,
    docs_loader=DocsLoader(),
)


@app.route('/api/v1/chat', methods=['POST'])
async def handle_message(request: Request):
    payload = ChatPayload(**request.json)
    rag_service.set_collection_name(payload.collection_name)

    async def stream_responses(resp):
        async for response_text in rag_service.get_answer(
                question=payload.messages_json(),  # type: ignore
                rag=payload.rag,
        ):
            await resp.write(json.dumps({'response': response_text}) + '\n')

    return ResponseStream(stream_responses, content_type='application/json')


@app.route('/api/v1/save', methods=['POST'])
async def save_in_db(request: Request):
    payload = SavePayload(
        files=request.files,  # type: ignore
        collection_name=request.form.get('collection_name'),  # type: ignore
    )
    validate_files(payload.files)

    files_paths = [
        await save_file(request.files.get(file)) for file in payload.files
    ]
    rag_service.set_collection_name(payload.collection_name)
    rag_service.create_collection(files_paths)

    for file_path in files_paths:
        os.remove(file_path)

    return response.json({'collection_id': rag_service.collection_name})
