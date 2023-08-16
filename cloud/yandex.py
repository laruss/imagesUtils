import yadisk

from cloud import settings
from core.utils import get_logger

logger = get_logger()
y = yadisk.YaDisk(token=settings.yandex.api_token)


def create_folder_if_not_exists(folder_path: str) -> None:
    logger.info(f"Creating folder: {folder_path}")
    try:
        y.mkdir(folder_path)
    except yadisk.exceptions.DirectoryExistsError:
        logger.info("Directory already exists, skipping")


def upload_zip_to_folder_name(
        folder_name: str,
        file_path: str,
        delete_if_exists: bool = True
) -> None:
    folder_path = f"/{folder_name}" if not folder_name.startswith("/") else folder_name
    zip_name = file_path.split("/")[-1]

    create_folder_if_not_exists(folder_path)

    if delete_if_exists:
        logger.info(f"Deleting {zip_name} if exists")
        try:
            y.remove(f"{folder_path}/{zip_name}")
        except yadisk.exceptions.PathNotFoundError:
            logger.info("File doesn't exist, skipping")

    logger.info(f"Uploading {zip_name} to {folder_path}")

    y.upload(file_path, f"{folder_path}/{zip_name}")

    logger.info(f"Uploaded {zip_name} to {folder_path}")


def download_zip_from_folder_name(folder_name: str, zip_path: str) -> None:
    logger.info(f"Downloading {zip_path} from {folder_name}")
    folder_path = f"/{folder_name}" if not folder_name.startswith("/") else folder_name
    zip_name = zip_path.split("/")[-1]

    y.download(f"{folder_path}/{zip_name}", zip_path)

    logger.info(f"Downloaded {zip_path} from {folder_name}")
