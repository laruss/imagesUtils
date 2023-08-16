import argparse
from enum import Enum

import core
from core.utils import get_logger
from cloud import settings, utils, yandex, google

parser = argparse.ArgumentParser()
logger = get_logger()
full_zip_path = f"{settings.temp_folder}/{settings.ZIP_NAME}"


class providers(Enum):
    yandex = "yandex"
    google = "google"


def upload(provider: providers):
    utils.zip_by_path(settings.final_folder, full_zip_path, settings.DELETE_AFTER_ZIP)

    if provider == providers.yandex:
        yandex.upload_zip_to_folder_name(settings.REMOTE_FOLDER_NAME, full_zip_path,
                                         settings.DELETE_REMOTE_ZIP_BEFORE_UPLOAD)
    elif provider == providers.google:
        client = google.GoogleDriveClient()
        client.upload_zip_to_folder_name(settings.REMOTE_FOLDER_NAME, full_zip_path,
                                         settings.DELETE_REMOTE_ZIP_BEFORE_UPLOAD)
    else:
        raise Exception(f"Unknown provider: {settings.PROVIDER}")


def download(provider: providers):
    if provider == providers.yandex:
        yandex.download_zip_from_folder_name(settings.REMOTE_FOLDER_NAME, full_zip_path)
    elif provider == providers.google:
        client = google.GoogleDriveClient()
        client.download_zip_from_folder_name(settings.REMOTE_FOLDER_NAME, full_zip_path)

    utils.unzip_by_path(full_zip_path, settings.final_folder, settings.DELETE_AFTER_UNZIP)


class methods(Enum):
    upload = "upload"
    download = "download"


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in methods],
                        required=True)
    parser.add_argument("--provider", help="provider", choices=[provider.name for provider in providers],
                        default=settings.PROVIDER)
    parser.add_argument("--silent", help="silent", action='store_true')


def main():
    add_arguments()
    args = parser.parse_args()

    logger.info(f"Using `{args.provider}` provider. Method: `{args.method}`")

    methods_map = {
        methods.upload: upload,
        methods.download: download,
    }

    methods_map[methods[args.method]](provider=providers[args.provider])
    core.utils.delete_file(full_zip_path)


if __name__ == '__main__':
    main()
