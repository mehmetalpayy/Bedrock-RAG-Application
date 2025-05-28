from pydantic import BaseModel


class ChatResponse(BaseModel):
    answer: str


class RetrievalResponse(BaseModel):
    answer: str