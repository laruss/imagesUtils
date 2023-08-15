from typing import Optional, List

from pydantic import BaseModel

from core.ProcessedItem import ProcessedItem
from download.models.scrolller.SubredditPost import SubredditPost


class SubredditChildren(BaseModel):
    iterator: Optional[str]
    items: List[SubredditPost]


class Subreddit(BaseModel):
    __typename: str
    id: int
    url: str
    title: str
    secondaryTitle: str
    description: str
    createdAt: Optional[str]
    isNsfw: bool
    subscribers: int
    isComplete: bool
    itemCount: int
    videoCount: int
    pictureCount: int
    albumCount: int
    isPaid: Optional[bool]
    username: Optional[str]
    tags: Optional[list]
    banner: Optional[list]
    isFollowing: Optional[bool]
    children: Optional[SubredditChildren]

    @property
    def posts_quantity(self):
        return len(self.children.items)

    def get_processed_posts(self) -> List[ProcessedItem]:
        return [post.get_processed() for post in self.children.items]
