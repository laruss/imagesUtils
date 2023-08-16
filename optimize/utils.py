import os

from PIL import Image

from optimize.settings import Settings
from core.utils import get_logger

logger = get_logger()


def one_to_webp(image_path: str, quality: int = 80, delete_original: bool = False) -> None:
    if not os.path.exists(image_path):
        raise Exception(f"File {image_path} does not exist.")

    with Image.open(image_path) as im:
        destination_path = os.path.splitext(image_path)[0] + ".webp"
        im.save(destination_path, "WEBP", quality=quality)
        if delete_original:
            os.remove(image_path)

        logger.info(f"Image {image_path} was converted.")


def to_webp(quality: int = 80, delete_original: bool = False) -> None:
    if not os.path.exists(Settings.images_folder):
        raise Exception(f"Folder {Settings.images_folder} does not exist.")

    image_files = [f for f in os.listdir(Settings.images_folder) if
                   os.path.isfile(os.path.join(Settings.images_folder, f)) and f.lower().endswith(('png', 'jpg', 'jpeg'))]

    logger.info(f"Found {len(image_files)} images.")

    for i, image_file in enumerate(image_files):
        one_to_webp(os.path.join(Settings.images_folder, image_file), quality, delete_original)
        logger.info(f"Processed {i + 1} of {len(image_files)} images")

    logger.info(f"Process is finished! {len(image_files)} of images were converted.")


def _get_file_size_in_kb(filepath):
    return os.path.getsize(filepath) / 1024


def minimize_one(
        image_path: str,
        image_final_size_kb: int = 512
) -> None:
    start_image_quality = 90

    if not os.path.exists(image_path):
        raise Exception(f"File {image_path} does not exist.")

    if _get_file_size_in_kb(image_path) > image_final_size_kb:  # for images larger than file size
        with Image.open(image_path) as im:
            quality = start_image_quality
            while _get_file_size_in_kb(image_path) > image_final_size_kb and quality > 10:
                im.save(image_path, "WEBP", quality=quality)
                quality -= 5  # Reduce quality by 5% per iteration
            logger.info(f"Image {image_path} was optimized, new size: {_get_file_size_in_kb(image_path)} KB")


def minimize(
        image_filter_size_kb: int = 1024,
        image_final_size_kb: int = 512,
        file_extension: str = '.webp'
) -> None:

    image_files = [f for f in os.listdir(Settings.images_folder) if
                   os.path.isfile(os.path.join(Settings.images_folder, f)) and f.lower().endswith(file_extension)]

    for image_file in image_files:
        file_path = os.path.join(Settings.images_folder, image_file)

        if _get_file_size_in_kb(file_path) > image_filter_size_kb:  # for images larger than file size
            minimize_one(file_path, image_final_size_kb)

    logger.info(f"Process is finished! {len(image_files)} of images were optimized.")
