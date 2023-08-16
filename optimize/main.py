import argparse

from core.utils import set_logger
from optimize import utils
from optimize.settings import Settings

parser = argparse.ArgumentParser()

methods = ['to_webp', 'minimize']


def add_arguments():
    parser.add_argument("--method", help="method", choices=methods, required=True)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()
    silent = args.silent or Settings.silent

    set_logger(not silent)

    if args.method == methods[0]:
        utils.to_webp(Settings.quality, Settings.delete_original)
    elif args.method == methods[1]:
        utils.minimize(Settings.image_filter_size_kb, Settings.image_final_size_kb, Settings.file_extension)
    else:
        raise Exception("Unknown method")


if __name__ == "__main__":
    main()
