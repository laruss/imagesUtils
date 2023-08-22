import os
from typing import Dict, List, BinaryIO

from PIL import Image
import imagehash

from core.utils import get_logger

logger = get_logger()


def get_files_hashes(folder_path: str) -> Dict[str, str]:
    """
    Get hashes of all files in folder
    :param folder_path:
    :return: dict {file_path: hash}
    """
    hashes = {}

    for dirname, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirname, filename)
            try:
                image = Image.open(file_path)
                h = str(imagehash.dhash(image))
                hashes[file_path] = h
            except Exception as e:
                logger.warning(f"Error processing file {file_path}: ({type(e)}){e}")

    return hashes


def get_duplicates_for_image(
    image: BinaryIO, hashes: Dict[str, str] = None, folder_path: str = None
) -> List[str]:
    """
    Find duplicates for image and return list of paths to duplicates
    :param image: BinaryIO
    :param hashes: dict {file_path: hash}
    :param folder_path: str, path to folder
    :return: list of paths to duplicates
    """

    assert hashes or folder_path, "Either hashes or folder_path should be provided"

    hashes = hashes or get_files_hashes(folder_path)
    duplicates = []

    image = Image.open(image)
    h = str(imagehash.dhash(image))

    for file_path, hash in hashes.items():
        if h == hash:
            duplicates.append(file_path)

    return duplicates


def get_duplicates_in_folder(folder_path: str) -> Dict[str, List[str]]:
    """
    Find duplicates in folder
    :param folder_path: str, path to folder
    :return: dict {hash: List[file_path]}
    """
    hashes = get_files_hashes(folder_path)
    duplicates = {}

    for file_path, hash in hashes.items():
        duplicates.setdefault(hash, []).append(file_path)

    return duplicates
