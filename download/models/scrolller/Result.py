from typing import List

from pydantic import BaseModel

from download.models.scrolller.Subreddit import Subreddit


class Result(BaseModel):
    iterator: str
    items: List[Subreddit]

    @property
    def posts_quantity(self):
        return sum(subreddit.posts_quantity for subreddit in self.items)
