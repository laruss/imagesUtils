#!/usr/bin/env python3

import argparse
from enum import Enum

import core
from core.utils import set_logger, get_logger

from download import utils, settings
from download.controllers import google, pexels, scrolller, pinterest

parser = argparse.ArgumentParser()
logger = get_logger()


class sources(Enum):
    pexels = pexels
    scrolller = scrolller
    google = google
    pinterest = pinterest


def add_arguments():
    parser.add_argument("--source", help="source site", choices=[source.name for source in sources],
                        required=True)
    parser.add_argument("--limit", help="limit of posts", type=int, default=settings.images_limit)
    parser.add_argument("--prompt", help="prompt for request", type=str, default=settings.prompt)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()

    set_logger(not args.silent)

    source = sources[args.source].value
    posts = source.get_items(limit=args.limit, query=args.prompt)

    for i, post in enumerate(posts):
        if args.limit and i >= args.limit:
            break

        data = core.utils.read_json_from_file(settings.data_file, False) or {}
        if str(post.id) in data.keys():
            logger.info(f"Skipping {post.id}, already in saved data")
            continue

        utils.download_image(post)
        data.update({post.id: post.model_dump()})
        core.utils.write_json_to_file(data, settings.data_file, rewrite=True)


if __name__ == "__main__":
    main()
