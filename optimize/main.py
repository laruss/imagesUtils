import argparse

from optimize import utils, settings

parser = argparse.ArgumentParser()

methods = ['to_webp', 'minimize']


def add_arguments():
    parser.add_argument("--method", help="method", choices=methods, required=True)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()
    silent = args.silent or settings.silent

    if args.method == methods[0]:
        utils.to_webp(settings.quality, settings.delete_original, silent=silent)
    elif args.method == methods[1]:
        utils.minimize(settings.image_filter_size_kb, settings.image_final_size_kb, settings.file_extension,
                       silent=silent)
    else:
        raise Exception("Unknown method")


if __name__ == "__main__":
    main()
