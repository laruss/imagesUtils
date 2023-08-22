from pydantic import BaseModel

from cloud.settings import CloudSettings
from core.utils import get_root_path, create_folder_if_not_exists, set_logger, read_json_from_file, write_json_to_file
from description.settings import DescriptionSettings
from download.settings import DownloadSettings
from optimize.settings import OptimizeSettings


class CoreSettings(BaseModel):
    final_folder: str = f"{get_root_path()}/static"
    temp_folder: str = f"{get_root_path()}/.tmp"
    images_folder: str = f"{final_folder}/images"
    data_file: str = f"{final_folder}/data.json"


class AllSettings(BaseModel):
    core: CoreSettings = CoreSettings()
    download: DownloadSettings = DownloadSettings()
    optimize: OptimizeSettings = OptimizeSettings()
    description: DescriptionSettings = DescriptionSettings()
    cloud: CloudSettings = CloudSettings()


# switch logging off or on and set the log file (if None, the log will be printed to the console)
set_logger(state=True, filename=None)

[create_folder_if_not_exists(folder) for folder in [CoreSettings().final_folder, CoreSettings().images_folder]]
if not read_json_from_file(CoreSettings().data_file, False):
    write_json_to_file({}, CoreSettings().data_file, True, True)
