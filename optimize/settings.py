from enum import Enum

from pydantic import BaseModel


class CartoonizeSettings(BaseModel):
    api_url: str = "https://cartoonize-lkqov62dia-de.a.run.app"
    api_cartoonize_path: str = "/cartoonize"
    api_final_path: str = "/static/cartoonized_images"
    pattern: str = r'<img src="static/cartoonized_images/(.*?)">'

    image_postfix: str = "_cartoonized"

    replace_original: bool = True


class Methods(str, Enum):
    to_webp = "to_webp"
    minimize = "minimize"
    delete_duplicates = "delete_duplicates"
    cartoonize = "cartoonize"


class OptimizeSettings(BaseModel):
    method: Methods = Methods.to_webp
    quality: int = 80
    delete_original: bool = True

    cartoonize: CartoonizeSettings = CartoonizeSettings()

    image_filter_size_kb: int = 1024
    image_final_size_kb: int = 512
    file_extension: str = ".webp"

    silent: bool = False
