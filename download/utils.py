from typing import List

import requests
from PIL import Image

from core.settings import CoreSettings
from core.utils import get_logger, read_json_from_file
from core.ProcessedItem import ProcessedItem

from download.controllers import Sources as ControllerSources
from download.settings import DownloadSettings
from optimize.duplicates import get_files_hashes

logger = get_logger()


class DownloadUtils:
    def __init__(self, settings: DownloadSettings = DownloadSettings(), core_settings: CoreSettings = CoreSettings()):
        self.settings = settings
        self.core_settings = core_settings

    @staticmethod
    def download_image(item: ProcessedItem) -> None:
        logger.info(f"Downloading image: {item.title or item.id} from {item.media}")

        raw_image = None
        image_path = f"{item._settings.core.images_folder}/{item.id}.jpg"

        try:
            raw_image = Image.open(requests.get(item.media, stream=True).raw).convert('RGB')
            raw_image.save(image_path)
        except Exception as e:
            logger.error(f"Skipping {item.id}, {e}")

        if raw_image:
            logger.info(f"Saved {item.media} to {item.image}")
            raw_image.close()

    def flow(self) -> List[ProcessedItem]:
        source = getattr(ControllerSources, self.settings.source.name)

        limit = self.settings.images_limit or 1
        prompt = self.settings.prompt

        items: List[ProcessedItem] = source(limit=limit, query=prompt)[:limit]
        processed_items = []

        hashes = get_files_hashes(self.core_settings.images_folder) if self.settings.check_duplicates else None
        for item in items:
            all_items_data = read_json_from_file(self.core_settings.data_file, False) or {}

            if str(item.id) in all_items_data.keys():
                logger.info(f"Skipping {item.id}, already in saved data")
                continue

            if self.settings.check_duplicates:
                duplicates = item.get_duplicates(hashes)
                if duplicates:
                    logger.info(f"Skipping {item.id}, duplicates found: {duplicates}")
                    continue

            self.download_image(item)
            item.save()
            processed_items.append(item)

        return processed_items
