# RAG-Chat
Chat backend for conversation about documents.

## Develop

### Start development
Initialize development environment
```bash
./bin/dev_init.sh
```

### Run server
To start development server you should use:
```bash
docker-compose up --build -d
```

### Useful scripts
In the repository there are many useful scripts, make sure you have containers running.

Example usage:
```bash
./bin/check.sh
```

| Script         | Comment                                                            |
|----------------|--------------------------------------------------------------------|
| check.sh       | Is running flake8, xenon, safety checks.                           |
| check_types.sh | Is running mypy check.                                             |
| dev_init.sh    | Is creating all development environment. Opposite of dev_clear.sh. |
| isort.sh       | Is for sort imports in python files.                               |
| security.sh    | Is running security checks.                                        |
| test.sh        | Is running tests.                                                  |


### Environment variables
| Name                      | Default            | Description                |
|---------------------------|--------------------|----------------------------|
| AZURE_OPENAI_API_KEY      |                    | Azure API key              |
| AZURE_OPENAI_ENDPOINT     |                    | Azure URL                  |
| OPENAI_API_VERSION        | 2024-03-01-preview | Azure API Version          |
| VECTOR_SIZE               | 1536               | Embedding vector size      |
| SENTRY_DSN                |                    | Sentry DSN                 |
| CHAT_DEPLOYMENT_NAME      | internalChat35     | Azure chat model name      |
| EMBEDDING_DEPLOYMENT_NAME |                    | Azure embedding model name |
| APP_VERSION               | 1.0.0              | Actual app version         |
| LOG_LEVEL                 | INFO               | Log level                  |
| QDRANT_HOST               | qdrant             | Qdrant host                |
| QDRANT_PORT               | 6333               | Qdrant port                |