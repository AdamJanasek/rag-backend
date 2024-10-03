from abc import ABC, abstractmethod
from typing import AsyncIterable

from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import BaseTransformOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


class AIServiceInterface(ABC):
    model: BaseChatModel

    @abstractmethod
    def chat_completion(
            self,
            prompt: ChatPromptTemplate,
            parser: BaseTransformOutputParser = StrOutputParser(),
            **kwargs,
    ) -> AsyncIterable[str]:
        raise NotImplementedError
