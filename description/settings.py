from decouple import config

from core.settings import *

IS_NSFW = 0.85

IMAGE_TO_TEXT_ENGINE = 'transformers'  # 'replicate' || 'transformers'


class sightengine:
    api_user: str = config('SIGHTENGINE_API_USER')
    api_secret: str = config('SIGHTENGINE_API_SECRET')
    models: str = 'nudity-2.0'


class replicate:
    api_token: str = config('REPLICATE_API_TOKEN')
