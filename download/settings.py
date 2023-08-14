from typing import Union

from decouple import config

from core.settings import *

images_limit = 50
prompt = "here some prompt"


class pexels:
    api_key: str = config['PEXELS_API_KEY']


class scroller:
    subreddit: Union[str, None] = "/r/Brawesome"  # e.g. "/r/lingerie" || None
    nsfw: bool = True


class google:
    api_key: str = config['GOOGLE_API_KEY']
    cx: str = config['GOOGLE_CX']
