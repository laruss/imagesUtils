from typing import List

import requests
from PIL import Image

from core.settings import CoreSettings
from core.utils import get_logger, read_json_from_file
from core.ProcessedItem import ProcessedItem

from download.controllers import Sources as ControllerSources
from download.settings import DownloadSettings


logger = get_logger()


def download_image(post: ProcessedItem, core_settings: CoreSettings = CoreSettings()) -> None:
    logger.info(f"Downloading image: {post.title}")

    raw_image = None
    image_path = f"{core_settings.images_folder}/{post.id}.jpg"

    try:
        raw_image = Image.open(requests.get(post.media, stream=True).raw).convert('RGB')
        raw_image.save(image_path)
    except Exception as e:
        logger.error(f"Skipping {post.id}, {e}")

    if raw_image:
        logger.info(f"Saved {post.media} to {image_path}")
        raw_image.close()


def flow(
        settings: DownloadSettings = DownloadSettings(),
        core_settings: CoreSettings = CoreSettings()
) -> List[ProcessedItem]:
    source = getattr(ControllerSources, settings.source.name)

    posts: List[ProcessedItem] = source(limit=settings.images_limit, query=settings.prompt)[:settings.images_limit]

    for post in posts:
        all_posts_data = read_json_from_file(core_settings.data_file, False) or {}

        if str(post.id) in all_posts_data.keys():
            logger.info(f"Skipping {post.id}, already in saved data")
            continue

        download_image(post, core_settings)
        post.save()

    return posts
