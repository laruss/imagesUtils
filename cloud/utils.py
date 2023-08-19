import os
import shutil

from cloud import yandex, google
from cloud.settings import Providers, CloudSettings, Methods
from core.settings import CoreSettings
from core.utils import get_logger, create_folder_if_not_exists, delete_file

logger = get_logger()
full_zip_path = f"{CoreSettings().temp_folder}/{CloudSettings().zip_name}"


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


def upload(settings: CloudSettings = CloudSettings(), core_settings: CoreSettings = CoreSettings()):
    zip_by_path(core_settings.final_folder, full_zip_path, settings.delete_after_zip)

    properties = (settings.remote_folder_name, full_zip_path, settings.delete_remote_zip_before_upload)

    if settings.provider == Providers.yandex:
        yandex.upload_zip_to_folder_name(*properties)
    elif settings.provider == Providers.google:
        client = google.GoogleDriveClient()
        client.upload_zip_to_folder_name(*properties)
    else:
        raise Exception(f"Unknown provider: {settings.provider.name}")


def download(settings: CloudSettings = CloudSettings(), core_settings: CoreSettings = CoreSettings()):
    properties = (settings.remote_folder_name, full_zip_path)

    if settings.provider == Providers.yandex:
        yandex.download_zip_from_folder_name(*properties)
    elif settings.provider == Providers.google:
        client = google.GoogleDriveClient()
        client.download_zip_from_folder_name(*properties)

    unzip_by_path(full_zip_path, core_settings.final_folder, settings.delete_after_zip)


def flow(settings: CloudSettings = CloudSettings(), core_settings: CoreSettings = CoreSettings()):
    logger.info(f"Using `{settings.provider.name}` provider. Method: `{settings.method.name}`")

    methods_map = {
        Methods.upload: upload,
        Methods.download: download,
    }

    methods_map[Methods[settings.method.name]](settings, core_settings)
    delete_file(full_zip_path)
