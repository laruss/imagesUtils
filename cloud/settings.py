from decouple import config

from core.settings import *

PROVIDER = 'google'  # 'yandex' || 'google'

REMOTE_FOLDER_NAME = 'images_utils_data'
ZIP_NAME = 'images_data.zip'

DELETE_AFTER_ZIP = False
DELETE_AFTER_UNZIP = False
DELETE_REMOTE_ZIP_BEFORE_UPLOAD = True


class yandex:
    api_token = config('YANDEX_API_TOKEN')


class google:
    local_server_port = 50607
