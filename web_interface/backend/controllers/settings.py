from typing import Union, Literal

from core.utils import read_json_from_file, write_json_to_file
from web_interface.backend.helpers.json_schema import JsonSchemaGenerator
from web_interface.backend.settings import settings_file_path, settings_data_schema_file_path

from download.settings import DownloadSettings as DownloadSettings
from optimize.settings import OptimizeSettings
from description.settings import DescriptionSettings
from cloud.settings import CloudSettings
from core.settings import CoreSettings


def _get_settings_models():
    return {
        'download': DownloadSettings,
        'optimize': OptimizeSettings,
        'description': DescriptionSettings,
        'cloud': CloudSettings,
        'core': CoreSettings
    }


def _get_settings_schema() -> dict:
    return read_json_from_file(settings_data_schema_file_path, False)


def _create_settings_schema() -> dict:
    models = _get_settings_models()
    schema = {}

    for model_name, model in models.items():
        schema[model_name] = model.model_json_schema(schema_generator=JsonSchemaGenerator)

    write_json_to_file(schema, settings_data_schema_file_path, True, True)

    return schema


def _get_settings_data() -> dict:
    return read_json_from_file(settings_file_path, False)


def _create_settings_data() -> dict:
    models = _get_settings_models()
    data = {}

    for model_name, model in models.items():
        data[model_name] = model().model_dump()

    write_json_to_file(data, settings_file_path, True, True)

    return data


def get_settings() -> dict:
    return _get_settings_data() or _create_settings_data()


def get_settings_as_model(
        model_name: Literal['download', 'optimize', 'description', 'cloud', 'core']
) -> Union[DownloadSettings, OptimizeSettings, DescriptionSettings, CloudSettings, CoreSettings]:
    models = _get_settings_models()

    return models[model_name](**get_settings()[model_name])


def get_settings_schema() -> dict:
    return _get_settings_schema() or _create_settings_schema()


def set_settings(new_data: dict) -> dict:
    get_settings()  # create settings file if it doesn't exist
    write_json_to_file(new_data, settings_file_path, rewrite=True)

    return new_data


def reset_settings() -> dict:
    return set_settings(_create_settings_data())
