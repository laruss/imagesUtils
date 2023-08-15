import argparse
from enum import Enum

from description.utils import describe, delete_nsfw
from description.gpt import gpt

parser = argparse.ArgumentParser()


class methods(Enum):
    describe = describe
    delete_nsfw = delete_nsfw
    gpt = gpt


def add_arguments():
    parser.add_argument("--method", help="method", choices=methods, required=True)


def main():
    add_arguments()
    args = parser.parse_args()


if __name__ == "__main__":
    main()
