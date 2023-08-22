from typing import Union

from core.utils import read_json_from_file, write_json_to_file
from web_interface.backend.helpers.json_schema import JsonSchemaGenerator
from web_interface.backend.settings import settings_file_path, settings_data_schema_file_path

from core.settings import AllSettings


def _get_settings_data() -> dict:
    return read_json_from_file(settings_file_path, False)


def _get_settings_schema_data() -> dict:
    return read_json_from_file(settings_data_schema_file_path, False)


def _write_settings_to_file(settings: dict = None) -> dict:
    settings = settings or AllSettings().model_dump()
    write_json_to_file(settings, settings_file_path, True, True)

    return _get_settings_data()


def _write_settings_schema_to_file() -> dict:
    schema = AllSettings().model_json_schema(schema_generator=JsonSchemaGenerator)
    write_json_to_file(schema, settings_data_schema_file_path, True, True)

    return _get_settings_schema_data()


def get_settings(as_data: bool = False) -> Union[AllSettings, dict]:
    settings_data = _get_settings_data() or _write_settings_to_file()

    return AllSettings(**settings_data) if not as_data else settings_data


def get_settings_schema() -> dict:
    return _get_settings_schema_data() or _write_settings_schema_to_file()


def set_settings(new_data: dict) -> dict:
    _ = AllSettings(**new_data)
    return _write_settings_to_file(new_data)


def reset_settings() -> dict:
    return set_settings(_write_settings_to_file())
