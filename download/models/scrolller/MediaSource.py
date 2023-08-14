from pydantic import BaseModel


class MediaSource(BaseModel):
    url: str
    width: int
    height: int
    isOptimized: bool
