from decouple import config

from core.settings import *
from description.prompts import Prompts

IS_NSFW = 0.85

IMAGE_TO_TEXT_ENGINE = 'transformers'  # 'replicate' || 'transformers'
SKIP_DESCRIPTION_IF_DESCRIBED = True
SKIP_GPT_IF_GPTED = True


class sightengine:
    api_user: str = config('SIGHTENGINE_API_USER')
    api_secret: str = config('SIGHTENGINE_API_SECRET')
    models: str = 'nudity-2.0'


class replicate:
    api_token: str = config('REPLICATE_API_TOKEN')


DEFAULT_PROMPT = Prompts.insta_post
GPT_MODEL = 'gpt-3.5-turbo'  # 'gpt-3.5-turbo' || 'gpt-4'
USED_GPT = 'gpt4free'  # 'gpt4free' || 'openai'


class openai:
    api_key = config('OPENAI_API_KEY')
