from core.settings import Settings
from core.utils import read_json_from_file, write_json_to_file, get_logger

logger = get_logger()


def get_image_path_by_id(image_id: str) -> str:
    """
    Returns the path to the image by its id.

    :param image_id: id of the image
    :return: path to the image
    """
    import glob

    return glob.glob(f"{Settings.images_folder}/{image_id}.*")[0]


def delete_image_data(image_id: str) -> None:
    """
    Deletes the image data by its id.

    :param image_id: id of the image
    :return: None
    """
    import os

    os.remove(get_image_path_by_id(image_id))

    data = read_json_from_file(Settings.data_file)
    del data[image_id]
    write_json_to_file(data, Settings.data_file, rewrite=True)

    logger.info(f"Image data for '{image_id}' successfully deleted.")
