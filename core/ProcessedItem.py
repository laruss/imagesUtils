from __future__ import annotations

import json
import logging
from typing import Optional, Union, Tuple, BinaryIO, List, Dict

import requests
from pydantic import BaseModel

from core.settings import AllSettings
from core.utils import get_logger
from description.prompt_schema import GPTResponseJSON
from optimize.duplicates import get_duplicates_for_image

logger = get_logger()


class ProcessedItem(BaseModel):
    _settings: AllSettings = AllSettings()
    _is_deleted: bool = False
    id: Union[int, str]
    title: str
    media: str
    description: Optional[str] = None
    gptJSON: Optional[GPTResponseJSON] = None
    gptText: Optional[str] = None

    @property
    def image(self) -> Optional[str]:
        """
        Get image path
        :return: str or None if image does not exist
        """
        from core.images_utils import get_image_path_by_id

        return get_image_path_by_id(self.id, self._settings.core.images_folder)

    def io_image(self, url: str = None) -> BinaryIO:
        """
        Get image as io
        :param url: str, url to image
        :return: BinaryIO
        """
        if self.image:
            return open(self.image, "rb")
        elif url:
            return requests.get(url, stream=True).raw
        else:
            raise Exception("Either image or url should be provided")

    def get_duplicates(self, hashes: Dict[str, str] = None) -> List[str]:
        """
        Get duplicates for image
        :param hashes: dict {file_path: hash}, if not provided, will be generated in get_duplicates_for_image
        :return: str, list of paths to duplicates
        """
        io_image = self.io_image(self.media)
        folder_path = self._settings.core.images_folder if not hashes else None
        duplicates = get_duplicates_for_image(
            io_image, folder_path=folder_path, hashes=hashes
        )

        if self.image and self.image in duplicates:
            duplicates.remove(self.image)

        return duplicates

    def describe(self) -> Tuple[str, bool]:
        """
        Describe image
        :return: description, bool whether description was generated
        """
        if not self.description:
            self.description = self.description_utils.describe(self)
            self.save()
            return self.description, True

        return self.description, False

    def gpt(self) -> Tuple[Optional[str], bool]:
        """
        Process image by gpt
        :return: gpt text, bool whether gpt text was generated
        """
        from description.gpt import gpt

        gpt_settings = self._settings.description.gpt_settings

        if not self.gptText or not gpt_settings.skip_gpt_if_gpted:
            self.gptText = gpt(self, gpt_settings)
            self.save()

            if self.gptText:
                return self.gptText, True

        return self.gptText, False

    def gpt2json(self, fall_if_failed: bool = False) -> Tuple[Optional[str], bool]:
        """
        Get gpt2json
        :param fall_if_failed: bool, whether to raise exception if gpt2json was not generated
        :return: gpt2json, bool whether json was generated
        """
        was_generated = False
        if not self._settings.description.gpt_settings.use_prompt_schema:
            logging.warning("Prompt schema is disabled, gpt2json will return None")

            return None, was_generated

        if not self.gptJSON:
            self.gptJSON = self.description_utils.gpt2json(self, fall_if_failed)
            self.save()

            if self.gptJSON:
                was_generated = True

        return json.dumps(self.gptJSON.model_dump(mode='json')), was_generated

    @property
    def optimize_utils(self):
        from optimize.utils import OptimizeUtils

        return OptimizeUtils(self._settings.optimize, self._settings.core)

    @property
    def download_utils(self):
        from download.utils import DownloadUtils

        return DownloadUtils(self._settings.download, self._settings.core)

    @property
    def description_utils(self):
        from description.utils import DescriptionUtils

        return DescriptionUtils(self._settings.description)

    def to_webp(self) -> Tuple[str, bool]:
        """
        Convert image to webp format
        :return: image path, bool whether image was converted
        """
        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        if image.endswith(".webp"):
            return image, False

        self.optimize_utils.one_to_webp(image)

        return self.image, True

    def minimize(self) -> Tuple[str, bool]:
        """
        Minimize image
        :return: path, bool whether image was minimized
        """
        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        return self.image, self.optimize_utils.minimize_one(image)

    def cartoonize(self) -> Tuple[str, bool]:
        """
        Cartoonize image
        :return: path, bool whether image was cartoonized
        """
        image = self.image
        if not image:
            raise Exception(f"File {image} does not exist.")

        return self.image, self.optimize_utils.cartoonize_one(image)

    def save(self, fall_on_fail: bool = False) -> None:
        """
        Save image data

        :param fall_on_fail: bool, whether to raise exception on fail
        :return: None
        """
        from core.utils import read_json_from_file, write_json_to_file, get_logger

        logger = get_logger()

        self.save_image(fall_on_fail)

        data = read_json_from_file(self._settings.core.data_file)
        data[self.id] = self.model_dump(mode="json")
        write_json_to_file(data, self._settings.core.data_file, rewrite=True)

        logger.info(f"Image data for '{self.id}' successfully saved.")

    def delete(self):
        """
        Delete image and its data
        :return: None
        """
        from core.images_utils import delete_image_data

        delete_image_data(self.id, self._settings.core.images_folder, self._settings.core.data_file)
        self._is_deleted = True
        logger.info(f"Image data for '{self.id}' successfully deleted.")

    def delete_nsfw(self) -> Tuple[str, bool]:
        """
        Delete image if it is nsfw
        :return: image path, bool whether image was deleted
        """
        return "", self.description_utils.delete_nsfw(self)

    def save_image(self, fall_on_fail: bool = False) -> None:
        """
        Save image and its data

        :param fall_on_fail: bool, whether to raise exception on fail
        :return: None
        """
        image = self.image
        if not image:
            self.download_utils.download_image(self, fall_on_fail)
            return None

        logger.info(f"Image file '{self.id}' already exists, skipping")
