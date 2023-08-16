import argparse
from enum import Enum

import core
from core.utils import get_logger
from cloud import utils, yandex, google
from cloud.settings import Settings

parser = argparse.ArgumentParser()
logger = get_logger()
full_zip_path = f"{Settings.temp_folder}/{Settings.zip_name}"


class providers(Enum):
    yandex = "yandex"
    google = "google"


def upload(provider: providers):
    utils.zip_by_path(Settings.final_folder, full_zip_path, Settings.delete_after_zip)

    properties = (Settings.remote_folder_name, full_zip_path, Settings.delete_remote_zip_before_upload)

    if provider == providers.yandex:
        yandex.upload_zip_to_folder_name(*properties)
    elif provider == providers.google:
        client = google.GoogleDriveClient()
        client.upload_zip_to_folder_name(*properties)
    else:
        raise Exception(f"Unknown provider: {Settings.provider}")


def download(provider: providers):
    properties = (Settings.remote_folder_name, full_zip_path)

    if provider == providers.yandex:
        yandex.download_zip_from_folder_name(*properties)
    elif provider == providers.google:
        client = google.GoogleDriveClient()
        client.download_zip_from_folder_name(*properties)

    utils.unzip_by_path(full_zip_path, Settings.final_folder, Settings.delete_after_zip)


class methods(Enum):
    upload = "upload"
    download = "download"


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in methods],
                        required=True)
    parser.add_argument("--provider", help="provider", choices=[provider.name for provider in providers],
                        default=Settings.provider)
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
