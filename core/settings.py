from core.utils import get_root_path, create_folder_if_not_exists

final_folder = f"{get_root_path()}/static"
images_folder = f"{final_folder}/images"
data_file = f"{final_folder}/data.json"

[create_folder_if_not_exists(folder) for folder in [final_folder, images_folder]]
