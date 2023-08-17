from typing import Optional, Union, Literal

from pydantic import BaseModel

from description.prompts import Prompts


class ProcessedItem(BaseModel):
    id: Union[int, str]
    title: str
    media: str
    description: Optional[str] = None
    gptJSON: Optional[dict] = None
    gptText: Optional[str] = None

    def describe(self, source: Literal['replicate', 'transformers']) -> str:
        from description.utils import describe

        if not self.description:
            self.description = describe(source, self)

            self.save()

        return self.description

    def process_by_gpt(self,
                       prompt: str,
                       model: Literal['gpt-4', 'gpt-3.5-turbo'] = 'gpt-3.5-turbo',
                       used_gpt: Literal['gpt4free', 'openai'] = 'gpt4free'
                       ) -> str:
        from description.gpt import gpt

        for prmpt in Prompts:
            if prmpt.value == prompt:
                prompt = prmpt
                break
        else:
            raise Exception(f"Prompt {prompt} not found")

        if not self.gptText:
            self.gptText = gpt(self, prompt, model, used_gpt)

            self.save()

        return self.gptText

    @property
    def image(self):
        from core.images_utils import get_image_path_by_id

        return get_image_path_by_id(self.id)

    def gpt2json(self) -> dict:
        from description.utils import gpt2json

        if not self.gptJSON:
            self.gptJSON = gpt2json(self)

            self.save()

        return self.gptJSON

    def to_webp(self, quality: int = 80, delete_original: bool = True) -> str:
        from optimize.utils import one_to_webp

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        if image.endswith('.webp'):
            return image

        one_to_webp(image, quality, delete_original)

        return self.image

    def optimize(self, image_final_size_kb: int = 512) -> str:
        from optimize.utils import minimize_one

        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        minimize_one(image, image_final_size_kb)

        return self.image

    def save(self) -> None:
        from core.utils import read_json_from_file, write_json_to_file, get_logger
        from core.settings import Settings

        logger = get_logger()

        data = read_json_from_file(Settings.data_file)
        data[self.id] = self.model_dump()
        write_json_to_file(data, Settings.data_file, rewrite=True)

        self.save_image()

        logger.info(f"Image data for '{self.id}' successfully saved.")

    def delete(self):
        from core.images_utils import delete_image_data

        delete_image_data(self.id)

    def save_image(self) -> None:
        from download.utils import download_image

        try:
            self.image
        except Exception:
            download_image(self)
