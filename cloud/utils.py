import os
import shutil

from core.utils import get_logger, create_folder_if_not_exists

logger = get_logger()


def zip_by_path(path: str, zippath: str, delete_after_zip: bool = False) -> str:
    if zippath.endswith(".zip"):
        zippath = zippath.replace(".zip", "")

    zip_name = zippath.split("/")[-1]
    path_to_zip = zippath.replace(zip_name, "")

    logger.info(f"Zipping {path} to {zippath}")

    create_folder_if_not_exists(path_to_zip)
    shutil.make_archive(zippath, 'zip', path)
    logger.info(f"Successfully zipped {path} to {zippath}")

    if delete_after_zip:
        shutil.rmtree(path)
        logger.info(f"Deleted {path}")

    return zippath


def unzip_by_path(zippath: str, path: str, delete_after_unzip: bool = False) -> str:
    logger.info(f"Unzipping {zippath} to {path}")

    shutil.unpack_archive(zippath, path)
    logger.info(f"Successfully unzipped {zippath} to {path}")

    if delete_after_unzip:
        os.remove(zippath)
        logger.info(f"Deleted {zippath}")

    return path
