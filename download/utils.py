import requests
from PIL import Image

from core.utils import get_logger
from download.settings import Settings
from core.ProcessedItem import ProcessedItem


logger = get_logger()


def download_image(post: ProcessedItem) -> None:
    logger.info(f"Downloading image: {post.title}")

    raw_image = None
    image_path = f"{Settings.images_folder}/{post.id}.jpg"

    try:
        raw_image = Image.open(requests.get(post.media, stream=True).raw).convert('RGB')
        raw_image.save(image_path)
    except Exception as e:
        logger.error(f"Skipping {post.id}, {e}")

    if raw_image:
        logger.info(f"Saved {post.media} to {image_path}")
        raw_image.close()
