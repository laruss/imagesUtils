import argparse
from enum import Enum

import download.settings as settings
from download import scrolller, pexels, utils, google

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

    [utils.download_image(post, args.silent) for post in posts]


if __name__ == "__main__":
    main()
