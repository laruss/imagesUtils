import re
from typing import Optional

import requests

from core.images_utils import download_from_url
from core.utils import get_logger
from optimize.settings import CartoonizeSettings

logger = get_logger()


def _get_image_id_from_response(
    response: requests.Response, pattern: str
) -> Optional[str]:
    """
    Get image id from response text

    :param response: requests.Response
    :param pattern: str, pattern for search
    :return: Optional[str], image id as "123324.jpg"
    """
    match = re.search(pattern, response.text)
    return match.group(1) if match else None


def cartoonize(
    image_path: str,
    final_path: str,
    settings: CartoonizeSettings = CartoonizeSettings(),
) -> bool:
    try:
        image = open(image_path, "rb")
    except FileNotFoundError:
        logger.error(f"Image with path '{image_path}' not found.")
        return False

    files = {"image": image}
    response = requests.post(
        f"{settings.api_url}{settings.api_cartoonize_path}", files=files
    )
    image_id = _get_image_id_from_response(response, settings.pattern)

    if not image_id:
        logger.error(f"Image id not found in response: {response.text}")
        return False

    image_url = f"{settings.api_url}{settings.api_final_path}/{image_id}"

    result = download_from_url(image_url, final_path)

    if result:
        logger.info(f"Image successfully cartoonized: {final_path}")
        return True
    else:
        logger.error(f"Image wasn't downloaded: {image_path}")
        return False
