import logging
import requests

from typing import List

from download import settings
from core.ProcessedItem import ProcessedItem
from download.models.pexels.Result import Result

logger = logging.getLogger()


def _get_items(query: str = "people", limit: int = 50) -> Result:
    logger.info(f"Getting {limit} items from pexels")

    headers = {
        "Authorization": settings.pexels.api_key,
    }
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={limit}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Error {response.status_code} when fetching items")

    result = response.json()

    logger.info(f"Got {len(result['photos'])} items")

    return Result(**result)


def get_items(limit: int = 50, query: str = "people") -> List[ProcessedItem]:
    photos = _get_items(limit=limit, query=query).photos

    return [ProcessedItem(id=item.id, title=item.alt, media=item.src['original']) for item in photos]
