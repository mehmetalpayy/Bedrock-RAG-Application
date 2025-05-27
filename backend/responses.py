from pydantic import BaseModel
from typing import List, Optional


class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    context: Optional[List[str]] = None


class RetrievalResponse(BaseModel):
    chunks: List[str]