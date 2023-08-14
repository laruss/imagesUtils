from typing import Union

from decouple import config

from core.utils import get_root_path

final_folder = f"{get_root_path()}/static"
images_folder = f"{final_folder}/images"
data_file = f"{final_folder}/data.json"

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
