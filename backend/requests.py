from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    user_input: str


class RetrievalRequest(BaseModel):
    query: str
    file_ids: Optional[List[str]] = None