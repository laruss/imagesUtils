import logging
from typing import Optional, Union

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

    def describe(self, settings: DescriptionInitSettings = DescriptionInitSettings()) -> str:
        from description.utils import describe

        if not self.description:
            self.description = describe(self, settings)
            self.save()

        return self.description

    def process_by_gpt(self, settings: GPTSettings = GPTSettings()) -> str:
        from description.gpt import gpt

        if not self.gptText or not settings.skip_gpt_if_gpted:
            self.gptText = gpt(self, settings)
            self.save()

        return self.gptText

    def gpt2json(self, settings: GPTSettings = GPTSettings()) -> Optional[dict]:
        from description.utils import gpt2json

        if not settings.use_prompt_schema:
            logging.warning("Prompt schema is disabled, gpt2json will return None")

            return None

        if not self.gptJSON:
            self.gptJSON = gpt2json(self)
            self.save()

        return self.gptJSON.model_dump() if self.gptJSON else None

    def to_webp(self, settings: OptimizeSettings = OptimizeSettings()) -> str:
        from optimize.utils import one_to_webp

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        if image.endswith('.webp'):
            return image

        one_to_webp(image, settings)

        return self.image

    def optimize(self, settings: OptimizeSettings = OptimizeSettings()) -> str:
        from optimize.utils import minimize_one

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        minimize_one(image, settings)

        return self.image

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

    def delete_if_nsfw(self, settings: NSFWDetectionSettings = NSFWDetectionSettings()) -> None:
        from description.utils import delete_nsfw

        delete_nsfw(self, settings)

    def save_image(self) -> None:
        from download.utils import download_image

        try:
            self.image
        except Exception:
            download_image(self)
