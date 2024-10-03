import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEFAULT_CHAT_DEPLOYMENT_NAME = 'gpt4o'
    DEFAULT_EMBEDDING_DEPLOYMENT_NAME = '3-large'

    CHAT_DEPLOYMENT_NAME = os.getenv(
        'CHAT_DEPLOYMENT_NAME',
        DEFAULT_CHAT_DEPLOYMENT_NAME,
    )
    EMBEDDING_DEPLOYMENT_NAME = os.getenv(
        'EMBEDDING_DEPLOYMENT_NAME',
        DEFAULT_EMBEDDING_DEPLOYMENT_NAME,
    )
    VECTOR_SIZE = int(os.getenv('VECTOR_SIZE', '3072'))
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    QDRANT_HOST = os.getenv('QDRANT_HOST', 'qdrant')
    QDRANT_PORT = int(os.getenv('QDRANT_PORT', '6333'))
