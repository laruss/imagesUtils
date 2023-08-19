import core.utils

modules = [
    'download',
    'optimize',
    'description',
    'cloud'
]


class server:
    host = 'localhost'
    port = 5002


server_path = f"{core.utils.get_root_path()}/web_interface"
backend_path = f"{server_path}/backend"
frontend_path = f"{server_path}/frontend"
models_path = f"{backend_path}/models"
settings_file_path = f"{models_path}/settings.json"
settings_data_schema_file_path = f"{models_path}/settings.json.schema.json"
image_data_schema_file_path = f"{models_path}/data.json.schema.json"
static_folder = f"{frontend_path}/build"
