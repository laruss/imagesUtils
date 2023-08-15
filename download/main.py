#!/usr/bin/env python3

import argparse
from enum import Enum

import core

from download import scrolller, pexels, utils, google, settings

parser = argparse.ArgumentParser()


class sources(Enum):
    pexels = 'pexels'
    scrolller = 'scrolller'
    google = 'google'


def add_arguments():
    parser.add_argument("--source", help="source site", choices=[source.value for source in sources],
                        required=True)
    parser.add_argument("--limit", help="limit of posts", type=int, default=settings.images_limit)
    parser.add_argument("--prompt", help="prompt for request", type=str, default=settings.prompt)
    parser.add_argument("--silent", help="silent mode", action="store_true")


def main():
    add_arguments()
    args = parser.parse_args()

    if args.source == sources.scrolller.value:
        posts = scrolller.get_posts(
            nsfw=settings.scroller.nsfw, limit=args.limit, subreddit=settings.scroller.subreddit, silent=args.silent)
    elif args.source == sources.pexels.value:
        posts = pexels.get_posts(limit=args.limit, query=args.prompt, silent=args.silent)
    elif args.source == sources.google.value:
        posts = google.get_posts(limit=args.limit, query=args.prompt, silent=args.silent)
    else:
        raise Exception("Unknown source")

    for i, post in enumerate(posts):
        if args.limit and i >= args.limit:
            break

        data = core.utils.read_json_from_file(core.settings.data_file, args.silent, False) or {}
        if str(post.id) in data.keys():
            if not args.silent:
                print(f"Skipping {post.id}, already in saved data")
            continue

        utils.download_image(post, args.silent)
        data.update({post.id: post.model_dump()})
        core.utils.write_json_to_file(data, core.settings.data_file, rewrite=True, silent=args.silent)


if __name__ == "__main__":
    main()
