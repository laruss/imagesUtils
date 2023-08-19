from pydantic import BaseModel

from core.utils import get_root_path, create_folder_if_not_exists, set_logger


class CoreSettings(BaseModel):
    final_folder: str = f"{get_root_path()}/static"
    temp_folder: str = f"{get_root_path()}/.tmp"
    images_folder: str = f"{final_folder}/images"
    data_file: str = f"{final_folder}/data.json"


# switch logging off or on and set the log file (if None, the log will be printed to the console)
set_logger(state=True, filename=None)

[create_folder_if_not_exists(folder) for folder in [CoreSettings().final_folder, CoreSettings().images_folder]]
