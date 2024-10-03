from typing import List, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatPayload(BaseModel):
    messages: List[ChatMessage]
    collection_name: str
    rag: Optional[bool] = False

    def messages_json(self):
        return [msg.model_dump() for msg in self.messages]
