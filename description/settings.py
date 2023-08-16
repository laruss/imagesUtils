import os

from decouple import Config, RepositoryEnv

import core.settings
from core.common import CommonSettings
from description.prompts import Prompts

dot_env_path = os.path.dirname(os.path.abspath(__file__)) + '/.env'
env_config = Config(RepositoryEnv(dot_env_path))


class sightengine(CommonSettings):
    api_user: str = env_config.get('SIGHTENGINE_API_USER')
    api_secret: str = env_config.get('SIGHTENGINE_API_SECRET')
    models: str = 'nudity-2.0'


class replicate(CommonSettings):
    api_token: str = env_config.get('REPLICATE_API_TOKEN')


class openai(CommonSettings):
    api_key = env_config.get('OPENAI_API_KEY')


class Settings(core.settings.Settings):
    is_nsfw = 0.85
    image_to_text_engine = 'transformers'  # 'replicate' || 'transformers'
    skip_description_if_described = True
    skip_gpt_if_gpted = True
    sightengine = sightengine()
    replicate = replicate()
    default_prompt = Prompts.insta_post.value
    gpt_model = 'gpt-3.5-turbo'  # 'gpt-3.5-turbo' || 'gpt-4'
    used_gpt = 'gpt4free'  # 'gpt4free' || 'openai'
    openai = openai()
