import os
from typing import Union

from decouple import Config, RepositoryEnv

import core.settings
from core.common import CommonSettings

dot_env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
env_config = Config(RepositoryEnv(dot_env_path))


class pexels(CommonSettings):
    api_key: str = env_config.get('PEXELS_API_KEY')


class scroller(CommonSettings):
    subreddit: Union[str, None] = "/r/Brawesome"  # e.g. "/r/lingerie" || None
    nsfw: bool = True


class google(CommonSettings):
    api_key: str = env_config.get('GOOGLE_API_KEY')
    cx: str = env_config.get('GOOGLE_CX')


class Settings(core.settings.Settings):
    images_limit = 50
    prompt = "fashion"
    pexels = pexels()
    scroller = scroller()
    google = google()
