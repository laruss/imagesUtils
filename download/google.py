import time
from typing import List

from google_images_search import GoogleImagesSearch

from download import settings
from download.models.ProcessedPost import ProcessedPost


def get_posts(limit: int = 50, query: str = "people", silent: bool = False) -> List[ProcessedPost]:
    gis = GoogleImagesSearch(settings.google.api_key, settings.google.cx)

    _search_params = {
        'q': query,
        'num': limit,
        'safe': 'off',
        'fileType': 'jpg|png|webp',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        'imgType': 'photo',
        'imgSize': 'xxlarge',
        'imgDominantColor': 'imgDominantColorUndefined',
        'imgColorType': 'imgColorTypeUndefined'
    }

    gis.search(search_params=_search_params)

    if not silent:
        print(f"Got {len(gis.results())} items")

    return [ProcessedPost(id=int(time.time()), title="no title", media=image.url) for image in gis.results()]
