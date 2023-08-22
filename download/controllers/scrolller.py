import logging
from typing import List

import requests

from core.ProcessedItem import ProcessedItem
from download.settings import DownloadSettings
from download.models.scrolller.Result import Result

logger = logging.getLogger()

query = [
    "query DiscoverSubredditsQuery( $filter: MediaFilter $limit: Int $iterator: String ) { discoverSubreddits( ",
    " filter: $filter limit: $limit iterator: $iterator ) { iterator items { __typename id url title secondaryTitle "
    "description createdAt isNsfw subscribers isComplete itemCount videoCount pictureCount albumCount isPaid username "
    "tags banner { url width height isOptimized } isFollowing children( limit: 2 iterator: null filter: PICTURE "
    "disabledHosts: null homePage: true ) { iterator items { __typename id url title subredditId subredditTitle "
    "subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource redgifsSource ownerAvatar "
    "username displayName isPaid tags isFavorite mediaSources { url width height isOptimized } blurredMediaSources "
    "{ url width height isOptimized } } } } } }",
]

query_for_subreddit = [
    " query SubredditQuery( $url: String! $filter: SubredditPostFilter $iterator: String ) { getSubreddit(url: $url) "
    "{ __typename id url title secondaryTitle description createdAt isNsfw subscribers isComplete itemCount videoCount "
    "pictureCount albumCount isPaid username tags banner { url width height isOptimized } isFollowing children"
    "( limit: 50 iterator: $iterator filter: $filter disabledHosts: null ) { iterator items { __typename id url title "
    "subredditId subredditTitle subredditUrl redditPath isNsfw albumUrl hasAudio fullLengthSource gfycatSource "
    "redgifsSource ownerAvatar username displayName isPaid tags isFavorite mediaSources "
    "{ url width height isOptimized } blurredMediaSources { url width height isOptimized } } } } } "
]

headers = {
    "content-type": "text/plain;charset=UTF-8",
    "accept": "*/*",
    "accept-language": "en",
    "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ",
}


def _get_items_by_subreddit(subreddit: str) -> Result:
    variables = {
        "url": subreddit,
        "filter": "PICTURE",
        "hostsDown": None,
    }

    data = {
        "query": query_for_subreddit[0],
        "variables": variables,
        "authorization": None,
    }

    response = requests.post(
        "https://api.scrolller.com/api/v2/graphql", json=data, headers=headers
    )

    if response.status_code != 200:
        raise Exception(
            f"Error {response.status_code} while fetching items from scrolller.com"
        )

    logger.info("Got items from scrolller.com")

    return Result(
        **{"iterator": "", "items": [response.json()["data"]["getSubreddit"]]}
    )


def _get_items(
    iterator: str = None, limit: int = 50, nsfw: bool = False, subreddit: str = None
) -> Result:
    logger.info(f"Fetching items from scrolller.com with iterator {iterator}")

    if subreddit:
        return _get_items_by_subreddit(subreddit)

    variables = {
        "filter": "PICTURE",
        "limit": limit,
        "hostsDown": None,
    }
    if iterator:
        variables["iterator"] = iterator

    data = {
        "query": query[0] + ("isNsfw: true" if nsfw else "isNsfw: false") + query[1],
        "variables": variables,
        "authorization": None,
    }

    response = requests.post(
        "https://api.scrolller.com/api/v2/graphql", json=data, headers=headers
    )

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} when fetching items")

    result = response.json()["data"]["discoverSubreddits"]

    logger.info(f"Got {len(result['items'])} items")

    return Result(**result)


def get_items(limit: int = 50, query: str = None) -> List[ProcessedItem]:
    settings = DownloadSettings()
    result_ = _get_items(
        nsfw=settings.scroller.nsfw, limit=limit, subreddit=settings.scroller.subreddit
    )
    posts_list = [item.get_processed_posts() for item in result_.items]

    return [post for posts in posts_list for post in posts]
