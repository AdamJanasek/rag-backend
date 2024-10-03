import time
from typing import AsyncIterable

from langchain_core.output_parsers import BaseTransformOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

from backend.interfaces.ai import AIServiceInterface
from backend.utils.logger import logger


class AzureAIService(AIServiceInterface):
    def __init__(self, deployment_name: str) -> None:
        self.model = AzureChatOpenAI(
            deployment_name=deployment_name,
            temperature=0,
            streaming=True,
        )  # type: ignore

    async def chat_completion(
            self,
            prompt: ChatPromptTemplate,
            parser: BaseTransformOutputParser = StrOutputParser(),
            **kwargs,
    ) -> AsyncIterable[str]:
        rag_chain = prompt | self.model | parser
        logger.info('Ask Azure AI...')
        start_time = time.time()

        for chunk in rag_chain.stream({**kwargs}):
            yield chunk
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f'Azure AI response received in {duration:.2f} seconds.')
