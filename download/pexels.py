from typing import List

import requests

from download import settings
from download.models.ProcessedPost import ProcessedPost
from download.models.pexels.Result import Result


def _get_items(query: str = "people", limit: int = 50, silent: bool = False) -> Result:
    if not silent:
        print(f"Getting {limit} items from pexels")
    headers = {
        "Authorization": settings.pexels.api_key,
    }
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Error {response.status_code} when fetching items")

    result = response.json()

    if not silent:
        print(f"Got {len(result['photos'])} items")

    return Result(**result)


def get_posts(limit: int = 50, query: str = "people", silent: bool = False) -> List[ProcessedPost]:
    photos = _get_items(limit=limit, query=query, silent=silent).photos

    return [ProcessedPost(id=item.id, title=item.alt, media=item.src['original']) for item in photos]
