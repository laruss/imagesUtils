import os
from enum import Enum

from decouple import Config, RepositoryEnv
from pydantic import BaseModel, SecretStr

dot_env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
env_config = Config(RepositoryEnv(dot_env_path))


class Sources(str, Enum):
    pexels = 'pexels'
    scrolller = 'scrolller'
    google = 'google'
    pinterest = 'pinterest'


class Pexels(BaseModel):
    api_key: SecretStr = env_config.get('PEXELS_API_KEY')


class Scroller(BaseModel):
    subreddit: str = "/r/Brawesome"  # e.g. "/r/lingerie" || None
    nsfw: bool = True


class Google(BaseModel):
    api_key: SecretStr = env_config.get('GOOGLE_API_KEY')
    cx: SecretStr = env_config.get('GOOGLE_CX')


class DownloadSettings(BaseModel):
    source: Sources = Sources.pinterest
    images_limit: int = 50
    prompt: str = "fashion"
    pexels: Pexels = Pexels()
    scroller: Scroller = Scroller()
    google: Google = Google()
