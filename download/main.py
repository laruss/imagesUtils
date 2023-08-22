#!/usr/bin/env python3

import argparse

from core.settings import CoreSettings
from core.utils import set_logger, get_logger

from download import utils
from download.settings import DownloadSettings, Sources
from download.utils import DownloadUtils

parser = argparse.ArgumentParser()
logger = get_logger()


def add_arguments():
    settings = DownloadSettings()
    parser.add_argument("--source", help="source site", choices=[source.name for source in Sources],
                        default=settings.source.name)
    parser.add_argument("--limit", help="limit of posts", type=int, default=settings.images_limit)
    parser.add_argument("--prompt", help="prompt for request", type=str, default=settings.prompt)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()

    set_logger(not args.silent)

    logger.info(f"Downloading images from `{args.source}` source, limit: {args.limit}, prompt: {args.prompt}")

    DownloadUtils(
        settings=DownloadSettings(
            source=Sources[args.source],
            images_limit=args.limit,
            prompt=args.prompt
        ),
        core_settings=CoreSettings()
    ).flow()


if __name__ == "__main__":
    main()
