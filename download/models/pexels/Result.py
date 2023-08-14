from typing import List

from pydantic import BaseModel

from download.models.pexels.Photo import Photo


class Result(BaseModel):
    page: int
    per_page: int
    photos: List[Photo]
