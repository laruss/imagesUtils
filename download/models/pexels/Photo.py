from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    width: int
    height: int
    url: str
    photographer: str
    photographer_url: str
    photographer_id: int
    avg_color: str
    src: dict
    liked: bool
    alt: str
