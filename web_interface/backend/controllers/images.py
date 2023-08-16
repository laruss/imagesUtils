from flask import send_file

from core.settings import Settings
from core.utils import read_json_from_file, write_json_to_file


def _get_data_schema():
    scheme = read_json_from_file(f"{Settings.data_file}.schema.json", False)

    return scheme


def _create_data_scheme_if_not_exists(data: dict):
    from genson import SchemaBuilder

    if _get_data_schema() is not None:
        return

    builder = SchemaBuilder()
    builder.add_object(data)

    schema = builder.to_schema()

    write_json_to_file(schema, f"{Settings.data_file}.schema.json", True, True)


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
