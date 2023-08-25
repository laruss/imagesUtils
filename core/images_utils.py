import glob
import os
import requests
from typing import Optional, Union

from PIL import Image

from core.utils import read_json_from_file, write_json_to_file, get_logger

logger = get_logger()


def get_image_path_by_id(image_id: str, images_folder_path: str) -> Optional[str]:
    """
    Returns the path to the image by its id.

    :param image_id: id of the image
    :param images_folder_path: path to the folder with images
    :return: path to the image
    """
    try:
        return glob.glob(f"{images_folder_path}/{image_id}.*")[0]
    except IndexError:
        logger.warning(f"Image with id '{image_id}' not found in path.")
        return None


def get_id_by_image_path(image_path: str) -> str:
    """
    Returns the id of the image by its path.

    :param image_path: str, path to the image
    :return: str, id of the image
    """
    return os.path.splitext(os.path.basename(image_path))[0]


def delete_image_data(
    image_id: str, images_folder_path: str, data_file_path: str
) -> None:
    """
    Deletes the image data by its id.

    :param image_id: id of the image
    :param images_folder_path: path to the folder with images
    :param data_file_path: path to the file with data
    :return: None
    """
    image_path = get_image_path_by_id(image_id, images_folder_path)

    os.remove(image_path) if image_path else logger.warning(
        f"Image with id '{image_id}' not found. Skipping deleting image file."
    )

    data = read_json_from_file(data_file_path)
    del data[image_id]
    write_json_to_file(data, data_file_path, rewrite=True)

    logger.info(f"Image data for '{image_id}' successfully deleted.")


def download_from_url(
    url: str, path: Union[str, os.PathLike], fall_on_fail: bool = False
) -> bool:
    """
    Download file from url to path

    :param url: str, url to download
    :param path: str, path to save
    :param fall_on_fail: bool, whether to raise exception on fail
    :return: None
    """
    raw_image = None

    try:
        raw_image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
        raw_image.save(path)
    except Exception as e:
        logger.error(f"Skipping {url}, {e}")
        if fall_on_fail:
            raise e

    if raw_image:
        logger.info(f"Saved {url} to {path}")
        raw_image.close()
        return True

    return False
