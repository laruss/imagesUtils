from typing import BinaryIO, Optional, List

import requests
import json

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

from core.ProcessedItem import ProcessedItem
from core.utils import get_logger
from description.prompt_schema import GPTResponseJSON
from description.settings import DescriptionSettings

logger = get_logger()


class DescriptionUtils:
    def __init__(self, settings: DescriptionSettings = DescriptionSettings()):
        self.settings = settings

    def _is_nsfw(self, io_image: BinaryIO):
        sightengine = self.settings.nsfw_settings.sightengine

        params = {
            "models": sightengine.models,
            "api_user": sightengine.api_user,
            "api_secret": sightengine.api_secret,
        }

        try:
            r = requests.post(sightengine.url, files=io_image, data=params)
        except Exception as e:
            logger.warning(f"NSFW check failed, {e}")

            return True

        result = json.loads(r.text)

        if not result["status"] == "success":
            logger.warning(f"NSFW check failed, status is {result['status']}")

            return False

        check = any(
            result["nudity"][key] > self.settings.is_nsfw
            for key in ["sexual_display", "sexual_activity", "erotica"]
        )
        method, text = (logger.warning, "failed") if check else (logger.info, "passed")
        method(f"NSFW check {text}, nsfw is {check}, {result['nudity']}")

        return check

    def _describe_item_replicate(self, io_image: BinaryIO) -> str:
        import replicate

        replicate_settings = self.settings.description_settings.replicate

        replicate.default_client.api_token = replicate_settings.api_token
        output = replicate.run(
            replicate_settings.api_model_version, input={"image": io_image}
        )

        return output.split(",")[0]

    def _describe_item_transformers(self, io_image: BinaryIO) -> str:
        transformers_settings = self.settings.description_settings.transformers

        processor = BlipProcessor.from_pretrained(transformers_settings.api_model_name)
        model = BlipForConditionalGeneration.from_pretrained(
            transformers_settings.api_model_name
        )

        raw_image = Image.open(io_image).convert("RGB")
        inputs = processor(raw_image, return_tensors="pt")

        out = model.generate(**inputs)

        return processor.decode(out[0], skip_special_tokens=True)

    def describe(self, item: ProcessedItem) -> Optional[str]:
        method = self.__getattribute__(
            f"_describe_item_{self.settings.description_settings.engine.name}"
        )

        logger.info(f"Describing item: {item.id}")

        try:
            result: Optional[str] = method(item.io_image())
        except Exception as e:
            logger.warning(f"Failed to describe item, {e}")
            result = None

        logger.info(f"Got description: {result}")

        return result

    def delete_nsfw(self, item: ProcessedItem) -> bool:
        """
        Delete item if nsfw is True
        :param item: ProcessedItem
        :return: bool, whether item was deleted
        """
        logger.info(f"Checking {item.id} for nsfw")

        if self._is_nsfw(item.io_image()):
            logger.warning(f"Deleting {item.id}, nsfw is True")
            item.delete()
            return True
        else:
            logger.info(f"Skipping {item.id}, nsfw is False")
            return False

    @staticmethod
    def gpt2json(item: ProcessedItem, fall_if_failed: bool = False) -> Optional[GPTResponseJSON]:
        """
        Get GPTResponseJSON from item
        :param item: ProcessedItem
        :param fall_if_failed: bool, whether to raise exception if failed
        :return: GPTResponseJSON or None
        """
        logger.info(f"Processing item: {item.id}")

        try:
            gpt_json = GPTResponseJSON(**json.loads(item.gptText))
        except Exception as e:
            logger.warning(f"Failed to process item, {e}")
            if fall_if_failed:
                raise e
            gpt_json = None

        logger.info(f"Got gpt json: {gpt_json}")

        return gpt_json

    def flow(self, items: List[ProcessedItem]) -> List[ProcessedItem]:
        """
        Main function for processing items

        :param items: list of ProcessedItems
        :return: list of ProcessedItems that were processed
        """
        item_processed = []

        for item in items:
            method = item.__getattribute__(f"{self.settings.method.name}")
            _, result = method()

            if result:
                item_processed.append(item)

        return item_processed
