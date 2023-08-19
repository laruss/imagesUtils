from flask import send_file

from core.ProcessedItem import ProcessedItem
from core.images_utils import get_image_path_by_id
from core.utils import read_json_from_file, write_json_to_file
from web_interface.backend.controllers.settings import get_settings_as_model
from web_interface.backend.settings import image_data_schema_file_path


def _get_data_schema():
    return read_json_from_file(image_data_schema_file_path, False)


def _create_data_schema() -> dict:
    from core.ProcessedItem import ProcessedItem

    schema = ProcessedItem.model_json_schema()

    write_json_to_file(schema, image_data_schema_file_path, True, True)

    return schema


def get_images_list():
    settings = get_settings_as_model('core')
    data_json = read_json_from_file(settings.data_file)

    return [id_ for id_ in data_json.keys()]


def get_image(image_id):
    return send_file(get_image_path_by_id(image_id), mimetype='image/jpeg')


def get_image_data(image_id):
    settings = get_settings_as_model('core')
    data_json = read_json_from_file(settings.data_file)
    image_data = data_json[str(image_id)]

    return image_data


def _get_image_model(image_id) -> ProcessedItem:
    return ProcessedItem(**get_image_data(image_id))


def get_image_data_schema():
    return _get_data_schema() or _create_data_schema()


def set_image_data(image_id, data):
    settings = get_settings_as_model('core')
    data_json = read_json_from_file(settings.data_file)
    _get_image_model(image_id)
    data_json[str(image_id)] = data
    write_json_to_file(data_json, settings.data_file, rewrite=True)

    return data_json[str(image_id)]


def generate_image_description(image_id: str):
    item = _get_image_model(image_id)
    settings = get_settings_as_model('description')

    item.describe(settings.description_settings)


def delete_image(image_id: str):
    item = _get_image_model(image_id)

    item.delete()


def process_by_gpt(image_id: str):
    item = _get_image_model(image_id)
    settings = get_settings_as_model('description')

    item.process_by_gpt(settings.gpt_settings)


def to_webp(image_id: str):
    item = _get_image_model(image_id)
    settings = get_settings_as_model('optimize')

    item.to_webp(settings)


def optimize_image(image_id: str):
    item = _get_image_model(image_id)
    settings = get_settings_as_model('optimize')

    item.optimize(settings)


def gpt2json(image_id: str):
    item = _get_image_model(image_id)
    settings = get_settings_as_model('description')

    item.gpt2json(settings.gpt_settings)
