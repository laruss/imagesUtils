import logging
from typing import Literal, Union, BinaryIO

import requests
import json

from core.ProcessedItem import ProcessedItem
from core.settings import images_folder
from description import settings


logger = logging.getLogger()


def _is_nsfw(path: str, silent: bool = False):
    params = {
        'models': settings.sightengine.models,
        'api_user': settings.sightengine.api_user,
        'api_secret': settings.sightengine.api_secret
    }
    url = 'https://api.sightengine.com/1.0/check.json'

    if not silent:
        print(f"Checking {path} for nsfw")
    try:
        files = {'media': open(path, 'rb')}
        r = requests.post(url, files=files, data=params)
    except Exception as e:
        print(e)
        return True

    result = json.loads(r.text)

    if not result['status'] == 'success':
        if not silent:
            print(f"WARNING: NSFW check failed, status is not success")
        return False

    if any(result['nudity'][key] > settings.IS_NSFW for key in ['sexual_display', 'sexual_activity', 'erotica']):
        if not silent:
            print(f"WARNING: NSFW check failed, nsfw is True, {result['nudity']}")
        return True
    else:
        if not silent:
            print(f"NSFW check passed, nsfw is False, {result['nudity']}")
        return False


def _describe_item_replicate(io_image: BinaryIO) -> str:
    import replicate

    replicate.default_client.api_token = settings.replicate.api_token
    output = replicate.run(
        "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5",
        input={"image": io_image}
    )

    return output.split(',')[0]


def _describe_item_transformers(io_image: BinaryIO) -> str:
    from PIL import Image
    from transformers import BlipProcessor, BlipForConditionalGeneration

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    raw_image = Image.open(io_image).convert('RGB')
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)

    return processor.decode(out[0], skip_special_tokens=True)


def _open_image_without_file_extension(image_name: Union[str, int]) -> BinaryIO:
    import glob

    image_path = glob.glob(f"{images_folder}{image_name}.*")[0]

    return open(image_path, 'rb')


def describe(source: Literal['replicate', 'transformers'], item: ProcessedItem) -> str:
    io_image = _open_image_without_file_extension(item.id)

    logger.info(f"Describing item: {item.id}")

    source_map = {
        'replicate': _describe_item_replicate,
        'transformers': _describe_item_transformers
    }
    result: str = source_map[source](io_image)

    logger.info(f"Got description: {result}")

    return result


def delete_nsfw(item: ProcessedItem) -> None:
    pass
