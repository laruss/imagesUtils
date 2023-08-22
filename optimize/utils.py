import os
from typing import List, Literal

from PIL import Image

from core.ProcessedItem import ProcessedItem
from core.images_utils import get_id_by_image_path
from core.settings import CoreSettings
from core.utils import get_logger
from optimize.cartoonize import cartoonize
from optimize.duplicates import get_files_hashes, get_duplicates_for_image
from optimize.settings import OptimizeSettings

logger = get_logger()


class OptimizeUtils:
    def __init__(
        self,
        settings: OptimizeSettings = OptimizeSettings(),
        core_settings: CoreSettings = CoreSettings(),
    ):
        self.settings = settings
        self.core_settings = core_settings

    @staticmethod
    def _get_file_size_in_kb(filepath):
        return os.path.getsize(filepath) / 1024

    def one_to_webp(self, image_path: str) -> None:
        """
        Convert one image to webp

        :param image_path: str, path to image
        :return: None
        """
        if not os.path.exists(image_path):
            raise Exception(f"File {image_path} does not exist.")

        with Image.open(image_path) as im:
            destination_path = os.path.splitext(image_path)[0] + ".webp"
            im.save(destination_path, "WEBP", quality=self.settings.quality)
            if self.settings.delete_original:
                os.remove(image_path)

            logger.info(f"Image {image_path} was converted.")

    def cartoonize_one(self, image_path: str) -> bool:
        """
        Cartoonize one image
        :param image_path: str, path to image
        :return: bool, whether image was cartoonized
        """
        if not os.path.exists(image_path):
            raise Exception(f"File {image_path} does not exist.")
        
        image_id = get_id_by_image_path(image_path)

        final_path = image_path \
            if self.settings.cartoonize.replace_original \
            else f"{self.core_settings.images_folder}/{image_id}{self.settings.cartoonize.image_postfix}.jpg"

        return cartoonize(image_path, final_path, self.settings.cartoonize)

    def minimize_one(self, image_path: str) -> bool:
        """
        Minimize image size

        :param image_path: str, path to image
        :return: bool whether image was minimized
        """
        start_image_quality = 90

        if not os.path.exists(image_path):
            raise Exception(f"File {image_path} does not exist.")

        if (
            self._get_file_size_in_kb(image_path) > self.settings.image_final_size_kb
        ):  # for images larger than file size
            with Image.open(image_path) as im:
                quality = start_image_quality
                while (
                    self._get_file_size_in_kb(image_path)
                    > self.settings.image_final_size_kb
                    and quality > 10
                ):
                    im.save(image_path, "WEBP", quality=quality)
                    quality -= 5  # Reduce quality by 5% per iteration
            logger.info(
                f"Image {image_path} was optimized, new size: {self._get_file_size_in_kb(image_path)} KB"
            )

            return True
        else:
            logger.info(
                f"Image {image_path} was not optimized, size: {self._get_file_size_in_kb(image_path)} KB"
            )

            return False

    @staticmethod
    def _to_webp_or_minimize(
        method_name: Literal["to_webp", "minimize"], items: List[ProcessedItem]
    ) -> List[ProcessedItem]:
        processed_items = []

        for item in items:
            image_path, result = item.minimize() if method_name == "minimize" else item.to_webp()

            if result:
                processed_items.append(item)

        return processed_items

    def to_webp(self, items: List[ProcessedItem]) -> List[ProcessedItem]:
        return self._to_webp_or_minimize("to_webp", items)

    def minimize(self, items: List[ProcessedItem]) -> List[ProcessedItem]:
        return self._to_webp_or_minimize("minimize", items)

    @staticmethod
    def delete_duplicates(items: List[ProcessedItem]) -> List[ProcessedItem]:
        duplicates = {}

        for item in items:
            for list_ in duplicates.values():
                if item.id in list_:
                    item.delete()

            if not item._is_deleted:
                duplicates[item.id] = item.get_duplicates()

        return [item for item in items if item._is_deleted]

    @staticmethod
    def cartoonize(items: List[ProcessedItem]) -> List[ProcessedItem]:
        processed_items = []

        for item in items:
            _, result = item.cartoonize()
            if result:
                processed_items.append(item)

        return processed_items

    def flow(self, items: List[ProcessedItem]) -> List[ProcessedItem]:
        return self.__getattribute__(self.settings.method.name)(items)
