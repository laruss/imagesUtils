import requests
from PIL import Image

from core.utils import *

from download import settings
from download.models.ProcessedPost import ProcessedPost


def download_image(post: ProcessedPost, silent: bool = True) -> None:
    if not silent:
        print(f"Downloading image: {post.title}")

    raw_image = None
    image_path = f"{settings.images_folder}/{post.id}.jpg"

    try:
        raw_image = Image.open(requests.get(post.media, stream=True).raw).convert('RGB')
        raw_image.save(image_path)
    except Exception as e:
        print(f"Skipping {post.id}, {e}")

    if raw_image:
        if not silent:
            print(f"Saved {post.media} to {image_path}")
        raw_image.close()
