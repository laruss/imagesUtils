import json
import logging
from typing import Optional, Union, Tuple

from pydantic import BaseModel

from description.prompt_schema import GPTResponseJSON
from description.settings import DescriptionInitSettings, GPTSettings, NSFWDetectionSettings
from optimize.settings import OptimizeSettings as OptimizeSettings


class ProcessedItem(BaseModel):
    id: Union[int, str]
    title: str
    media: str
    description: Optional[str] = None
    gptJSON: Optional[GPTResponseJSON] = None
    gptText: Optional[str] = None

    @property
    def image(self) -> str:
        from core.images_utils import get_image_path_by_id

        return get_image_path_by_id(self.id)

    def describe(self, settings: DescriptionInitSettings = DescriptionInitSettings()) -> Tuple[str, bool]:
        """
        Describe image
        :param settings:
        :return: description, bool whether description was generated
        """
        from description.utils import describe

        if not self.description:
            self.description = describe(self, settings)
            self.save()
            return self.description, True

        return self.description, False

    def process_by_gpt(self, settings: GPTSettings = GPTSettings()) -> Tuple[Optional[str], bool]:
        from description.gpt import gpt

        if not self.gptText or not settings.skip_gpt_if_gpted:
            self.gptText = gpt(self, settings)
            self.save()

            if self.gptText:
                return self.gptText, True

        return self.gptText, False

    def gpt2json(self, settings: GPTSettings = GPTSettings()) -> Tuple[Optional[str], bool]:
        from description.utils import gpt2json

        if not settings.use_prompt_schema:
            logging.warning("Prompt schema is disabled, gpt2json will return None")

            return None, False

        if not self.gptJSON:
            self.gptJSON = gpt2json(self)
            self.save()

            if self.gptJSON:
                return json.dumps(self.gptJSON.model_dump()), True

        return json.dumps(self.gptJSON.model_dump()), False

    def to_webp(self, settings: OptimizeSettings = OptimizeSettings()) -> Tuple[str, bool]:
        """
        Convert image to webp format
        :param settings:
        :return: image path, bool whether image was converted
        """
        from optimize.utils import one_to_webp

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        if image.endswith('.webp'):
            return image, False

        one_to_webp(image, settings)

        return self.image, True

    def optimize(self, settings: OptimizeSettings = OptimizeSettings()) -> Tuple[str, bool]:
        from optimize.utils import minimize_one

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        return self.image, minimize_one(image, settings)

    def save(self) -> None:
        from core.utils import read_json_from_file, write_json_to_file, get_logger
        from core.settings import CoreSettings

        logger = get_logger()

        core_settings = CoreSettings()

        data = read_json_from_file(core_settings.data_file)
        data[self.id] = self.model_dump()
        write_json_to_file(data, core_settings.data_file, rewrite=True)

        self.save_image()

        logger.info(f"Image data for '{self.id}' successfully saved.")

    def delete(self):
        from core.images_utils import delete_image_data

        delete_image_data(self.id)

    def delete_if_nsfw(self, settings: NSFWDetectionSettings = NSFWDetectionSettings()) -> Tuple[str, bool]:
        from description.utils import delete_nsfw

        return '', delete_nsfw(self, settings)

    def save_image(self) -> None:
        from download.utils import download_image

        try:
            self.image
        except Exception:
            download_image(self)
