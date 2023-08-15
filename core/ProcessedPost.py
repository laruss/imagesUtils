from typing import Optional

from pydantic import BaseModel


class ProcessedPost(BaseModel):
    id: int
    title: str
    media: str
    description: Optional[str]
    gptJSON: Optional[dict]
    gptText: Optional[str]

