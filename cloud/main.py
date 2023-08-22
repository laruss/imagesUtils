import argparse

from cloud.utils import CloudUtils
from core.settings import CoreSettings
from core.utils import get_logger, set_logger
from cloud.settings import CloudSettings, Providers, Methods

parser = argparse.ArgumentParser()
logger = get_logger()


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in Methods],
                        default=CloudSettings.method.name)
    parser.add_argument("--provider", help="provider", choices=[provider.name for provider in Providers],
                        default=CloudSettings.provider.name)
    parser.add_argument("--silent", help="silent", action='store_true')


def main():
    add_arguments()
    args = parser.parse_args()

    set_logger(not args.silent)

    CloudUtils(
        CloudSettings(
            method=Methods[args.method],
            provider=Providers[args.provider]
        ),
        CoreSettings()
    ).flow()


if __name__ == '__main__':
    main()
