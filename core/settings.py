from core.utils import get_root_path, create_folder_if_not_exists, set_logger

final_folder = f"{get_root_path()}/static"
images_folder = f"{final_folder}/images"
data_file = f"{final_folder}/data.json"

# switch logging off or on
set_logger(True)

[create_folder_if_not_exists(folder) for folder in [final_folder, images_folder]]
