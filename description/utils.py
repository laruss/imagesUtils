from typing import Literal, Union, BinaryIO, Optional

import replicate
import requests
import json
import glob

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from core.ProcessedItem import ProcessedItem
from core.images_utils import get_image_path_by_id, delete_image_data
from core.utils import read_json_from_file, write_json_to_file, get_logger
from description.settings import Settings

logger = get_logger()


def _is_nsfw(io_image: BinaryIO):
    params = {
        'models': Settings.sightengine.models,
        'api_user': Settings.sightengine.api_user,
        'api_secret': Settings.sightengine.api_secret
    }
    url = 'https://api.sightengine.com/1.0/check.json'

    try:
        r = requests.post(url, files=io_image, data=params)
    except Exception as e:
        logger.warning(f"NSFW check failed, {e}")

        return True

    result = json.loads(r.text)

    if not result['status'] == 'success':
        logger.warning(f"NSFW check failed, status is {result['status']}")

        return False

    check = any(result['nudity'][key] > Settings.is_nsfw for key in ['sexual_display', 'sexual_activity', 'erotica'])
    method, text = (logger.warning, 'failed') if check else (logger.info, 'passed')
    method(f"NSFW check {text}, nsfw is {check}, {result['nudity']}")

    return check


def _describe_item_replicate(io_image: BinaryIO) -> str:
    replicate.default_client.api_token = Settings.replicate.api_token
    output = replicate.run(
        "methexis-inc/img2prompt:50adaf2d3ad20a6f911a8a9e3ccf777b263b8596fbd2c8fc26e8888f8a0edbb5",
        input={"image": io_image}
    )

    return output.split(',')[0]


def _describe_item_transformers(io_image: BinaryIO) -> str:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    raw_image = Image.open(io_image).convert('RGB')
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)

    return processor.decode(out[0], skip_special_tokens=True)


def _open_image_without_file_extension(image_name: Union[str, int]) -> BinaryIO:
    image_path = glob.glob(f"{Settings.images_folder}{image_name}.*")[0]

    return open(image_path, 'rb')


def describe(source: Literal['replicate', 'transformers'], item: ProcessedItem) -> Optional[str]:
    image_path = get_image_path_by_id(item.id)
    io_image = open(image_path, 'rb')

    logger.info(f"Describing item: {item.id}")

    source_map = {
        'replicate': _describe_item_replicate,
        'transformers': _describe_item_transformers
    }

    try:
        result: Optional[str] = source_map[source](io_image)
    except Exception as e:
        logger.warning(f"Failed to describe item, {e}")
        result = None

    logger.info(f"Got description: {result}")

    return result


def delete_nsfw(item: ProcessedItem) -> None:
    logger.info(f"Checking {item.id} for nsfw")

    image_path = get_image_path_by_id(item.id)
    io_image = open(image_path, 'rb')

    if _is_nsfw(io_image):
        logger.warning(f"Deleting {item.id}, nsfw is True")
        delete_image_data(item.id)
    else:
        logger.info(f"Skipping {item.id}, nsfw is False")


def save_item(item: ProcessedItem) -> None:
    logger.info(f"Saving item: {item.id}")

    items_dict = read_json_from_file(Settings.data_file, error_on_invalid_json=False) or {}

    items_dict[str(item.id)] = item.model_dump()

    write_json_to_file(items_dict, Settings.data_file, rewrite=True)


def gpt2json(item: ProcessedItem) -> Optional[Union[dict, list]]:
    logger.info(f"Processing item: {item.id}")

    try:
        gpt_json = json.loads(item.gptText)
    except Exception as e:
        logger.warning(f"Failed to process item, {e}")
        gpt_json = None

    logger.info(f"Got gpt json: {gpt_json}")

    return gpt_json
