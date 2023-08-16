from core.utils import read_json_from_file, write_json_to_file
from web_interface.backend.settings import settings_file_path


def _create_settings_file(data: dict = None):
    data = data or {}
    write_json_to_file(data, settings_file_path, True, True)


def _generate_init_data_scheme(data: dict) -> None:
    from genson import SchemaBuilder

    builder = SchemaBuilder()
    builder.add_object(data)

    schema = builder.to_schema()

    write_json_to_file(schema, f"{settings_file_path}.schema.json", True, True)


def _get_init_data():
    from download.settings import Settings as DownloadSettings
    from optimize.settings import Settings as OptimizeSettings
    from description.settings import Settings as DescriptionSettings
    from cloud.settings import Settings as CloudSettings
    from core.settings import Settings as CoreSettings

    exclude_fields = ['final_folder', 'temp_folder', 'images_folder', 'data_file', 'logger', 'log_file']

    return {
        'download': DownloadSettings.get_dict(*exclude_fields),
        'optimize': OptimizeSettings.get_dict(*exclude_fields),
        'description': DescriptionSettings.get_dict(*exclude_fields),
        'cloud': CloudSettings.get_dict(*exclude_fields),
        'core': CoreSettings.get_dict()
    }


def _get_settings_file() -> dict:
    data = read_json_from_file(settings_file_path, False)
    if data is None:
        data = _get_init_data()
        _create_settings_file(data)
        _generate_init_data_scheme(data)

    return data


def get_settings() -> dict:
    # if there are no settings.json file in 'models' folder, create one
    return _get_settings_file()


def set_settings(new_data: dict) -> dict:
    from jsonschema import validate

    schema = read_json_from_file(f"{settings_file_path}.schema.json", False)

    if schema is None:
        raise Exception("Schema file is missing. Please, contact the developer.")

    validate(new_data, schema)

    _create_settings_file(new_data)

    return new_data
