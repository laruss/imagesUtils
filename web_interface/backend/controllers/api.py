from download.utils import flow as download_flow
from optimize.utils import flow as optimize_flow
from description.utils import flow as description_flow
from cloud.utils import flow as cloud_flow
from web_interface.backend.controllers.settings import get_settings_as_model
from web_interface.backend.helpers.utils import get_images_models


def download_images():
    settings = get_settings_as_model('download')
    download_flow(settings)


def optimize_images():
    items = get_images_models()
    settings = get_settings_as_model('optimize')
    optimize_flow(items, settings)


def describe_images():
    items = get_images_models()
    settings = get_settings_as_model('description')
    description_flow(items, settings)


def cloud_images():
    settings = get_settings_as_model('cloud')
    core_settings = get_settings_as_model('core')
    cloud_flow(settings, core_settings)
