import requests
from PIL import Image

from download import settings
from core.ProcessedItem import ProcessedItem


def download_image(post: ProcessedItem, silent: bool = True) -> None:
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
