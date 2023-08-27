import logging
import time
from typing import List

from google_images_search import GoogleImagesSearch

from download.settings import DownloadSettings
from core.ProcessedItem import ProcessedItem


logger = logging.getLogger()


def get_items(limit: int = 50, query: str = "people") -> List[ProcessedItem]:
    download_settings = DownloadSettings()
    gis = GoogleImagesSearch(
        download_settings.google.api_key.get_secret_value(), download_settings.google.cx.get_secret_value()
    )

    _search_params = {
        "q": query,
        "num": limit,
        "safe": "off",
        "fileType": "jpg|png|webp",
        "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
        "imgType": "photo",
        "imgSize": "xxlarge",
        "imgDominantColor": "imgDominantColorUndefined",
        "imgColorType": "imgColorTypeUndefined",
    }

    gis.search(search_params=_search_params)

    logger.info(f"Fetching items from google.com with query '{query}'")

    return [
        ProcessedItem(id=int(time.time()), title="no title", media=image.url)
        for image in gis.results()
    ]
