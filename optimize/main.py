import argparse

from core.ProcessedItem import ProcessedItem
from core.settings import CoreSettings
from core.utils import set_logger, read_json_from_file
from optimize.utils import OptimizeUtils
from optimize.settings import OptimizeSettings, Methods

parser = argparse.ArgumentParser()


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in Methods],
                        default=OptimizeSettings().method.name)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()

    core_settings = CoreSettings()
    optimize_settings = OptimizeSettings(method=Methods[args.method])

    silent = args.silent or optimize_settings.silent

    set_logger(not silent)

    items = read_json_from_file(core_settings.data_file, False) or {}

    OptimizeUtils(optimize_settings, core_settings) \
        .flow(items=[ProcessedItem(**val) for key, val in items.items()])


if __name__ == "__main__":
    main()
