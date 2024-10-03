from typing import List

from langchain_openai import AzureOpenAIEmbeddings

from backend.interfaces.embedding import EmbeddingServiceInterface


class AzureEmbeddingService(EmbeddingServiceInterface):

    def __init__(self, deployment_name: str) -> None:
        self.model = AzureOpenAIEmbeddings(model=deployment_name)

    def get_embedding(self, text: str) -> List[float]:
        return self.model.embed_query(text)
