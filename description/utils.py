from typing import BinaryIO, Optional, List

import replicate
import requests
import json

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from core.ProcessedItem import ProcessedItem
from core.utils import read_json_from_file, write_json_to_file, get_logger
from description.prompt_schema import GPTResponseJSON
from description.settings import DescriptionSettings, Methods, DescriptionInitSettings, NSFWDetectionSettings
from core.settings import CoreSettings

logger = get_logger()


def _is_nsfw(io_image: BinaryIO, settings: NSFWDetectionSettings = NSFWDetectionSettings()):
    params = {
        'models': settings.sightengine.models,
        'api_user': settings.sightengine.api_user,
        'api_secret': settings.sightengine.api_secret
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

    check = any(result['nudity'][key] > DescriptionSettings().is_nsfw for key in ['sexual_display', 'sexual_activity', 'erotica'])
    method, text = (logger.warning, 'failed') if check else (logger.info, 'passed')
    method(f"NSFW check {text}, nsfw is {check}, {result['nudity']}")

    return check


def _describe_item_replicate(io_image: BinaryIO) -> str:
    replicate.default_client.api_token = DescriptionSettings().replicate.api_token
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


def describe(item: ProcessedItem, settings: DescriptionInitSettings = DescriptionInitSettings()) -> Optional[str]:
    io_image = open(item.image, 'rb')

    logger.info(f"Describing item: {item.id}")

    source_map = {
        'replicate': _describe_item_replicate,
        'transformers': _describe_item_transformers
    }

    try:
        result: Optional[str] = source_map[settings.engine.name](io_image)
    except Exception as e:
        logger.warning(f"Failed to describe item, {e}")
        result = None

    logger.info(f"Got description: {result}")

    return result


def delete_nsfw(item: ProcessedItem, settings: NSFWDetectionSettings = NSFWDetectionSettings()) -> None:
    logger.info(f"Checking {item.id} for nsfw")

    io_image = open(item.image, 'rb')

    if _is_nsfw(io_image, settings):
        logger.warning(f"Deleting {item.id}, nsfw is True")
        item.delete()
    else:
        logger.info(f"Skipping {item.id}, nsfw is False")


def save_item(item: ProcessedItem) -> None:
    logger.info(f"Saving item: {item.id}")

    core_settings = CoreSettings()

    items_dict = read_json_from_file(core_settings.data_file, error_on_invalid_json=False) or {}

    items_dict[str(item.id)] = item.model_dump()

    write_json_to_file(items_dict, core_settings.data_file, rewrite=True)


def gpt2json(item: ProcessedItem) -> Optional[GPTResponseJSON]:
    logger.info(f"Processing item: {item.id}")

    try:
        gpt_json = GPTResponseJSON(**json.loads(item.gptText))
    except Exception as e:
        logger.warning(f"Failed to process item, {e}")
        gpt_json = None

    logger.info(f"Got gpt json: {gpt_json}")

    return gpt_json


def flow(items: List[ProcessedItem], settings: DescriptionSettings = DescriptionSettings()):
    """
    Main function for processing items

    :param items: list of ProcessedItems
    :param settings: Settings
    :return: None
    """
    for item in items:

        mapping = {
            Methods.describe: (item.describe, settings.description_settings),
            Methods.delete_nsfw: (item.delete_if_nsfw, settings.nsfw_settings),
            Methods.gpt: (item.process_by_gpt, settings.gpt_settings),
            Methods.gpt2json: (item.gpt2json, settings.gpt_settings)
        }

        method, parameter = mapping[settings.method]
        method(parameter)
