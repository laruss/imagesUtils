from cloud.settings import CloudSettings, Methods as CloudMethods
from description.settings import Methods as DescriptionMethods
from download.utils import flow as download_flow
from optimize.settings import OptimizeSettings, Methods as OptimizeMethods
from optimize.utils import flow as optimize_flow
from description.utils import flow as description_flow
from cloud.utils import flow as cloud_flow
from web_interface.backend.controllers.settings import get_settings_as_model
from web_interface.backend.helpers.utils import get_images_models


def download_images() -> str:
    settings = get_settings_as_model('download')
    core_settings = get_settings_as_model('core')
    items_processed = download_flow(settings, core_settings)

    return f"Downloaded {len(items_processed)} items"


def optimize_images():
    items = get_images_models()
    settings: OptimizeSettings = get_settings_as_model('optimize')
    items_processed = optimize_flow(items, settings)
    method = "webp-ed" if settings.method == OptimizeMethods.to_webp else "compressed"

    return f"{method.capitalize()} {len(items_processed)} items"


def describe_images():
    items = get_images_models()
    settings = get_settings_as_model('description')
    items_processed = description_flow(items, settings)

    mappings = {
        DescriptionMethods.describe: "described",
        DescriptionMethods.delete_nsfw: "deleted as nsfw",
        DescriptionMethods.gpt: "described with gpt",
        DescriptionMethods.gpt2json: "gpt json created",
    }

    return f"{mappings[settings.method].capitalize()} {len(items_processed)} items"


def cloud_images():
    settings: CloudSettings = get_settings_as_model('cloud')
    core_settings = get_settings_as_model('core')

    items = []

    if settings.method == CloudMethods.upload:
        items = get_images_models()

    cloud_flow(settings, core_settings)

    if settings.method == CloudMethods.download:
        items = get_images_models()

    method = "uploaded" if settings.method == CloudMethods.upload else "downloaded"

    return f"{method.capitalize()} {len(items)} items"
