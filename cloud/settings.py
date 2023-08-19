import os
from enum import Enum

from decouple import Config, RepositoryEnv
from pydantic import BaseModel, SecretStr

dot_env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
env_config = Config(RepositoryEnv(dot_env_path))


class Methods(str, Enum):
    upload = "upload"
    download = "download"


class Yandex(BaseModel):
    api_token: SecretStr = env_config.get('YANDEX_API_TOKEN')


class Google(BaseModel):
    local_server_port: int = 50607


class Providers(str, Enum):
    yandex = 'yandex'
    google = 'google'


class CloudSettings(BaseModel):
    method: Methods = Methods.upload
    provider: Providers = Providers.yandex
    remote_folder_name: str = 'images_utils_data'
    zip_name: str = 'images_data.zip'
    delete_after_zip: bool = False
    delete_after_unzip: bool = False
    delete_remote_zip_before_upload: bool = True
    yandex: Yandex = Yandex()
    google: Google = Google()
