from cloud.settings import Methods as CloudMethods
from description.settings import Methods as DescriptionMethods
from download.utils import DownloadUtils
from optimize.settings import Methods as OptimizeMethods
from optimize.utils import OptimizeUtils
from description.utils import DescriptionUtils
from cloud.utils import CloudUtils
from web_interface.backend.controllers.settings import get_settings
from web_interface.backend.helpers.utils import get_images_models


def download_images() -> str:
    settings = get_settings()
    items_processed = DownloadUtils(settings.download, settings.core).flow()

    return f"Downloaded {len(items_processed)} items"


def optimize_images(method: OptimizeMethods = OptimizeMethods.to_webp) -> str:
    items = get_images_models()
    settings = get_settings()
    settings.optimize.method = method
    items_processed = OptimizeUtils(settings.optimize, settings.core).flow(items)

    return f"Method '{method.name}' was applied to {len(items_processed)} items"


def describe_images(method: DescriptionMethods = DescriptionMethods.describe) -> str:
    items = get_images_models()
    settings = get_settings().description
    settings.method = method
    items_processed = DescriptionUtils(settings).flow(items)

    return f"Method {method.name} was applied to {len(items_processed)} items"


def cloud_images(method: CloudMethods = CloudMethods.upload) -> str:
    settings = get_settings()
    settings.cloud.method = method

    items = []

    if settings.cloud.method == CloudMethods.upload:
        items = get_images_models()

    CloudUtils(settings.cloud, settings.core).flow()

    if settings.cloud.method == CloudMethods.download:
        items = get_images_models()

    method = "uploaded" if settings.cloud.method == CloudMethods.upload else "downloaded"

    return f"{method.capitalize()} {len(items)} items"
