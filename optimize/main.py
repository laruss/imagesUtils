import argparse

from core.ProcessedItem import ProcessedItem
from core.settings import CoreSettings
from core.utils import set_logger, read_json_from_file
from optimize import utils
from optimize.settings import OptimizeSettings, Methods

parser = argparse.ArgumentParser()


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in Methods],
                        default=OptimizeSettings().method.name)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()
    silent = args.silent or OptimizeSettings().silent

    set_logger(not silent)

    items = read_json_from_file(CoreSettings().data_file, False) or {}

    utils.flow(
        items=[ProcessedItem(**val) for key, val in items.items()],
        settings=OptimizeSettings(
            method=Methods[args.method]
        )
    )


if __name__ == "__main__":
    main()
