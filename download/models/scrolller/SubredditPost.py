from typing import Optional, List

from pydantic import BaseModel

from download.models.scrolller.MediaSource import MediaSource
from core.ProcessedItem import ProcessedItem


class SubredditPost(BaseModel):
    __typename: str
    id: int
    url: str
    title: str
    subredditId: int
    subredditTitle: str
    subredditUrl: str
    redditPath: str
    isNsfw: bool
    albumUrl: Optional[str]
    hasAudio: Optional[bool]
    fullLengthSource: Optional[str]
    gfycatSource: Optional[str]
    redgifsSource: Optional[str]
    ownerAvatar: Optional[str]
    username: Optional[str]
    displayName: Optional[str]
    isPaid: Optional[bool]
    tags: Optional[list]
    isFavorite: Optional[bool]
    mediaSources: List[MediaSource]

    @property
    def get_biggest_media(self):
        return max(self.mediaSources, key=lambda x: x.width * x.height)

    def get_processed(self) -> ProcessedItem:
        return ProcessedItem(
            id=self.id, title=self.title, media=self.get_biggest_media.url
        )
