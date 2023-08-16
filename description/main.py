import argparse
from enum import Enum

from core.ProcessedItem import ProcessedItem
from core.utils import set_logger, read_json_from_file, get_logger
from description import settings
from description.utils import describe, delete_nsfw, save_item, gpt2json
from description.gpt import gpt

parser = argparse.ArgumentParser()
logger = get_logger()

class methods(Enum):
    describe = "describe"
    delete_nsfw = "delete_nsfw"
    gpt = "gpt"
    gpt2json = "gpt2json"


def add_arguments():
    parser.add_argument("--method", help="method", choices=[method.name for method in methods], required=True)
    parser.add_argument("--gpt-model", help="gpt model", choices=['gpt-4', 'gpt-3.5-turbo'], default=settings.GPT_MODEL)
    parser.add_argument("--used-gpt", help="used gpt", choices=['gpt4free', 'openai'], default=settings.USED_GPT)
    parser.add_argument("--silent", help="silent", action='store_true')


def main():
    add_arguments()
    args = parser.parse_args()

    set_logger(not args.silent)

    method = methods[args.method]
    items = read_json_from_file(settings.data_file, False) or {}

    logger.info(f"Processing {len(items)} items, using `{method.name}` method.")

    for key, val in items.items():
        prc_item = ProcessedItem(**val)

        if method == methods.describe:
            if settings.SKIP_DESCRIPTION_IF_DESCRIBED and prc_item.description:
                logger.info(f"Skipping {prc_item.id}, already described")
                continue
            prc_item.description = describe(settings.IMAGE_TO_TEXT_ENGINE, prc_item)
            save_item(prc_item)
        elif method == methods.delete_nsfw:
            delete_nsfw(prc_item)
        elif method == methods.gpt:
            if settings.SKIP_GPT_IF_GPTED and prc_item.gptText:
                logger.info(f"Skipping {prc_item.id}, already GPTed")
                continue
            prc_item.gptText = gpt(prc_item,
                                   prompt=settings.DEFAULT_PROMPT, model=args.gpt_model, used_gpt=args.used_gpt)
            save_item(prc_item)
        elif method == methods.gpt2json:
            prc_item.gptJSON = gpt2json(prc_item)
            save_item(prc_item)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    main()
