from typing import Literal

from flask import send_file

from core.ProcessedItem import ProcessedItem
from core.settings import Settings
from core.utils import read_json_from_file, write_json_to_file
from web_interface.backend.settings import data_schema_file_path


def _get_data_schema():
    scheme = read_json_from_file(data_schema_file_path, False)

    return scheme


def _create_data_scheme_if_not_exists(data: dict):
    from genson import SchemaBuilder

    if _get_data_schema() is not None:
        return

    builder = SchemaBuilder()
    builder.add_object(data)

    schema = builder.to_schema()

    write_json_to_file(schema, data_schema_file_path, True, True)


def _get_image_path_by_id_without_extension(image_id: str):
    import glob

    return glob.glob(f"{Settings.images_folder}/{image_id}.*")[0]


def get_images_list():
    data_json = read_json_from_file(Settings.data_file)

    return [id_ for id_ in data_json.keys()]


def get_image(image_id):
    path = _get_image_path_by_id_without_extension(image_id)

    return send_file(path, mimetype='image/jpeg')


def get_image_data(image_id):
    data_json = read_json_from_file(Settings.data_file)

    image_data = data_json[str(image_id)]

    _create_data_scheme_if_not_exists(image_data)

    return image_data


def set_image_data(image_id, data):
    from jsonschema import validate

    schema = _get_data_schema()

    if schema is None:
        raise Exception("Schema file is missing. Please, contact the developer.")

    validate(data, schema)

    data_json = read_json_from_file(Settings.data_file)
    data_json[str(image_id)] = data
    write_json_to_file(data_json, Settings.data_file, rewrite=True)

    return data_json[str(image_id)]


def generate_image_description(image_id: str, source: Literal['replicate', 'transformers']):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.describe(source)


def delete_image(image_id: str):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.delete()


def process_by_gpt(image_id: str, prompt: str,
                   model: Literal['gpt-4', 'gpt-3.5-turbo'] = 'gpt-3.5-turbo',
                   used_gpt: Literal['gpt4free', 'openai'] = 'gpt4free'
                   ):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.process_by_gpt(prompt, model, used_gpt)


def to_webp(image_id: str, quality: int = 80, delete_original: bool = True):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.to_webp(quality, delete_original)


def optimize_image(image_id: str, image_final_size_kb: int = 512):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.optimize(image_final_size_kb)


def gpt2json(image_id: str):
    data_json = read_json_from_file(Settings.data_file)
    item = ProcessedItem(**data_json[str(image_id)])
    item.gpt2json()
