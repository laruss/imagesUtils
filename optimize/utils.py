import os

from PIL import Image

from core.settings import *


def to_webp(quality: int = 80, delete_original: bool = False, silent: bool = False) -> None:
    if not os.path.exists(images_folder):
        raise Exception(f"Folder {images_folder} does not exist.")

    image_files = [f for f in os.listdir(images_folder) if
                   os.path.isfile(os.path.join(images_folder, f)) and f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not silent:
        print(f"Found {len(image_files)} images.")

    for i, image_file in enumerate(image_files):
        with Image.open(os.path.join(images_folder, image_file)) as im:
            destination_path = os.path.join(images_folder, os.path.splitext(image_file)[0] + ".webp")
            im.save(destination_path, "WEBP", quality=quality)
            if delete_original:
                os.remove(os.path.join(images_folder, image_file))

            if not silent:
                print(f"Image {image_file} was converted. {i + 1} of {len(image_files)}")

    if not silent:
        print(f"Process is  finished! {len(image_files)} of images were converted.")


def minimize(
        image_filter_size_kb: int = 1024,
        image_final_size_kb: int = 512,
        file_extension: str = '.webp',
        silent: bool = False
) -> None:
    start_image_quality = 90

    def get_file_size_in_kb(filepath):
        return os.path.getsize(filepath) / 1024

    image_files = [f for f in os.listdir(images_folder) if
                   os.path.isfile(os.path.join(images_folder, f)) and f.lower().endswith(file_extension)]

    for image_file in image_files:
        file_path = os.path.join(images_folder, image_file)

        if get_file_size_in_kb(file_path) > image_filter_size_kb:  # for images larger than file size
            with Image.open(file_path) as im:
                quality = start_image_quality
                while get_file_size_in_kb(file_path) > image_final_size_kb and quality > 10:
                    im.save(file_path, "WEBP", quality=quality)
                    quality -= 5  # Reduce quality by 5% per iteration
                if not silent:
                    print(f"Image {image_file} was optimized, new size: {get_file_size_in_kb(file_path)} KB")

    if not silent:
        print("Process is  finished!")

