import os
from enum import Enum

from decouple import Config, RepositoryEnv
from pydantic import BaseModel, SecretStr, Field

from description.prompts import Prompts

dot_env_path = os.path.dirname(os.path.abspath(__file__)) + "/.env"
env_config = Config(RepositoryEnv(dot_env_path))


class Sightengine(BaseModel):
    api_user: int = Field(int(env_config.get("SIGHTENGINE_API_USER")), min=0)
    api_secret: SecretStr = Field(
        env_config.get("SIGHTENGINE_API_SECRET"), min_length=20, max_length=20
    )
    models: str = "nudity-2.0"
    url: str = "https://api.sightengine.com/1.0/check.json"


class Replicate(BaseModel):
    api_token: SecretStr = env_config.get("REPLICATE_API_TOKEN")
    api_model_version: str = "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5"


class Transformers(BaseModel):
    api_model_name: str = "Salesforce/blip-image-captioning-base"


class Openai(BaseModel):
    api_key: SecretStr = env_config.get("OPENAI_API_KEY")


class ImageToTextEngine(str, Enum):
    transformers = "transformers"
    replicate = "replicate"


class GPTModel(str, Enum):
    gpt35turbo = "gpt-3.5-turbo"
    gpt4 = "gpt-4"


class Service(str, Enum):
    gpt4free = "gpt4free"
    openai = "openai"


class Methods(str, Enum):
    describe = "describe"
    delete_nsfw = "delete_nsfw"
    gpt = "gpt"
    gpt2json = "gpt2json"


class NSFWDetectionSettings(BaseModel):
    sightengine: Sightengine = Sightengine()
    nsfw_level_to_detect: float = 0.85


class DescriptionInitSettings(BaseModel):
    replicate: Replicate = Replicate()
    transformers: Transformers = Transformers()

    engine: ImageToTextEngine = ImageToTextEngine.transformers
    skip_description_if_described: bool = True


class GPTSettings(BaseModel):
    openai: Openai = Openai()

    service: Service = Service.gpt4free
    model: GPTModel = GPTModel.gpt35turbo
    prompt: Prompts = Prompts.default
    skip_gpt_if_gpted: bool = True
    use_prompt_schema: bool = True


class DescriptionSettings(BaseModel):
    method: Methods = Methods.describe

    nsfw_settings: NSFWDetectionSettings = NSFWDetectionSettings()
    description_settings: DescriptionInitSettings = DescriptionInitSettings()
    gpt_settings: GPTSettings = GPTSettings()
