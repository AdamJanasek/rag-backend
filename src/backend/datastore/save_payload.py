from pydantic import BaseModel
from sanic.request import RequestParameters


class SavePayload(BaseModel):
    files: RequestParameters
    collection_name: str

    class Config:
        arbitrary_types_allowed = True
