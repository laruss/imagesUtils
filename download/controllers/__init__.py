from enum import Enum

from . import google, pexels, scrolller, pinterest


class Sources(str, Enum):
    pexels = pexels.get_items
    scrolller = scrolller.get_items
    google = google.get_items
    pinterest = pinterest.get_items


__all__ = ['Sources']
