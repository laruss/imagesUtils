import argparse

from core.ProcessedItem import ProcessedItem
from core.settings import CoreSettings
from core.utils import set_logger, read_json_from_file, get_logger

from description.settings import DescriptionSettings, Methods, GPTModel, Service, GPTSettings
from description.utils import DescriptionUtils

parser = argparse.ArgumentParser()
logger = get_logger()


def add_arguments():
    settings = DescriptionSettings()
    parser.add_argument("--method", help="method", choices=[method.name for method in Methods],
                        default=settings.method.name)
    parser.add_argument("--gpt-model", help="gpt model", choices=[model.name for model in GPTModel],
                        default=settings.gpt_model.name)
    parser.add_argument("--used-gpt", help="used gpt", choices=[service.name for service in Service],
                        default=settings.used_gpt.name)
    parser.add_argument("--silent", help="silent", action='store_true')


def main():
    add_arguments()
    args = parser.parse_args()

    set_logger(not args.silent)

    method = Methods[args.method]
    items = read_json_from_file(CoreSettings().data_file, False) or {}

    logger.info(f"Processing {len(items)} items, using `{method.name}` method.")

    DescriptionUtils(
        settings=DescriptionSettings(
            method=method,
            gpt_settings=GPTSettings(
                model=GPTModel[args.gpt_model],
                service=Service[args.used_gpt]
            )
        )
    ).flow(items=[ProcessedItem(**val) for key, val in items.items()])


if __name__ == "__main__":
    main()
