import os
import shutil

from cloud import yandex, google
from cloud.settings import Providers, CloudSettings
from core.settings import CoreSettings
from core.utils import get_logger, create_folder_if_not_exists, delete_file

logger = get_logger()


class CloudUtils:
    def __init__(self, settings: CloudSettings = CloudSettings(), core_settings: CoreSettings = CoreSettings()):
        self.settings = settings
        self.core_settings = core_settings
        self.full_zip_path = f"{core_settings.temp_folder}/{settings.zip_name}"

    def zip_by_path(self, path: str, delete_after_zip: bool = False) -> str:
        zippath = self.full_zip_path

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

    def unzip_by_path(self, path: str, delete_after_unzip: bool = False) -> str:
        zippath = self.full_zip_path

        logger.info(f"Unzipping {zippath} to {path}")

        shutil.unpack_archive(zippath, path)
        logger.info(f"Successfully unzipped {zippath} to {path}")

        if delete_after_unzip:
            os.remove(zippath)
            logger.info(f"Deleted {zippath}")

        return path

    def upload(self):
        self.zip_by_path(self.core_settings.final_folder, self.settings.delete_after_zip)

        properties = (self.settings.remote_folder_name, self.full_zip_path, self.settings.delete_remote_zip_before_upload)

        if self.settings.provider == Providers.yandex:
            yandex.upload_zip_to_folder_name(*properties)
        elif self.settings.provider == Providers.google:
            client = google.GoogleDriveClient()
            client.upload_zip_to_folder_name(*properties)
        else:
            raise Exception(f"Unknown provider: {self.settings.provider.name}")

    def download(self):
        properties = (self.settings.remote_folder_name, self.full_zip_path)

        if self.settings.provider == Providers.yandex:
            yandex.download_zip_from_folder_name(*properties)
        elif self.settings.provider == Providers.google:
            client = google.GoogleDriveClient()
            client.download_zip_from_folder_name(*properties)

        self.unzip_by_path(self.core_settings.final_folder, self.settings.delete_after_zip)

    def flow(self):
        logger.info(f"Using `{self.settings.provider.name}` provider. Method: `{self.settings.method.name}`")

        method = self.__getattribute__(f"{self.settings.method.name}")

        method()
        delete_file(self.full_zip_path)
