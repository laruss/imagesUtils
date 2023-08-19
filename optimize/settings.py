from enum import Enum

from pydantic import BaseModel


class Methods(str, Enum):
    to_webp = 'to_webp'
    minimize = 'minimize'


class OptimizeSettings(BaseModel):
    method: Methods = Methods.to_webp
    quality: int = 80
    delete_original: bool = True

    image_filter_size_kb: int = 1024
    image_final_size_kb: int = 512
    file_extension: str = '.webp'

    silent: bool = False
