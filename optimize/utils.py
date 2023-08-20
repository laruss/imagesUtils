import os
from typing import List

from PIL import Image

from core.ProcessedItem import ProcessedItem
from core.utils import get_logger
from optimize.settings import OptimizeSettings, Methods

logger = get_logger()


def one_to_webp(image_path: str, settings: OptimizeSettings = OptimizeSettings()) -> None:
    if not os.path.exists(image_path):
        raise Exception(f"File {image_path} does not exist.")

    with Image.open(image_path) as im:
        destination_path = os.path.splitext(image_path)[0] + ".webp"
        im.save(destination_path, "WEBP", quality=settings.quality)
        if settings.delete_original:
            os.remove(image_path)

        logger.info(f"Image {image_path} was converted.")


def _get_file_size_in_kb(filepath):
    return os.path.getsize(filepath) / 1024


def minimize_one(image_path: str, settings: OptimizeSettings = OptimizeSettings()) -> bool:
    """
    Minimize image size

    :param image_path:
    :param settings:
    :return: bool whether image was minimized
    """
    start_image_quality = 90

    if not os.path.exists(image_path):
        raise Exception(f"File {image_path} does not exist.")

    if _get_file_size_in_kb(image_path) > settings.image_final_size_kb:  # for images larger than file size
        with Image.open(image_path) as im:
            quality = start_image_quality
            while _get_file_size_in_kb(image_path) > settings.image_final_size_kb and quality > 10:
                im.save(image_path, "WEBP", quality=quality)
                quality -= 5  # Reduce quality by 5% per iteration
        logger.info(f"Image {image_path} was optimized, new size: {_get_file_size_in_kb(image_path)} KB")

        return True
    else:
        logger.info(f"Image {image_path} was not optimized, size: {_get_file_size_in_kb(image_path)} KB")

        return False


def flow(items: List[ProcessedItem], settings: OptimizeSettings = OptimizeSettings()) -> List[ProcessedItem]:
    processed_items = []

    for item in items:
        if settings.method == Methods.to_webp:
            image_path, result = item.to_webp(settings)
        elif settings.method == Methods.minimize:
            image_path, result = item.optimize(settings)
        else:
            raise Exception("Unknown method")

        if result:
            processed_items.append(item)

    return processed_items
