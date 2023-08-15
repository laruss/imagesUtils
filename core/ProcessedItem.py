from typing import Optional, Union

from pydantic import BaseModel


class ProcessedItem(BaseModel):
    id: Union[int, str]
    title: str
    media: str
    description: Optional[str] = None
    gptJSON: Optional[dict] = None
    gptText: Optional[str] = None

