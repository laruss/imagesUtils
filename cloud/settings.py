import os

from decouple import Config, RepositoryEnv

import core.settings
from core.common import CommonSettings


dot_env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
env_config = Config(RepositoryEnv(dot_env_path))


class yandex(CommonSettings):
    api_token = env_config.get('YANDEX_API_TOKEN')


class google(CommonSettings):
    local_server_port = 50607


class Settings(core.settings.Settings):
    provider = 'google'  # 'yandex' || 'google'
    remote_folder_name = 'images_utils_data'
    zip_name = 'images_data.zip'
    delete_after_zip = False
    delete_after_unzip = False
    delete_remote_zip_before_upload = True
    yandex = yandex()
    google = google()
