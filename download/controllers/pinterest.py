import json
import logging
from typing import Dict, Literal, List

import requests

from core.ProcessedItem import ProcessedItem
from download.models.pinterest import Options, Model

URL = 'https://pinterest.com/resource/BaseSearchResource/get/'

logger = logging.getLogger()


def _get_data(query: str = None, options: Options = None) -> Dict[Literal["options", "context"], dict]:
    assert query or options, "Either query or options must be provided"

    options = options or Options(
        bookmarks=None, article="", appliedProductFilters="---", price_max=None, price_min=None, query=query,
        scope="pins", auto_correction_disabled="", top_pin_id="", filters=""
    )

    return {
        "options": options.model_dump(),
        "context": {}
    }


def _get_model(data: Dict[Literal["options", "context"], dict]) -> Model:
    source_url = "/search/pins/?rs=ac"

    logger.info(f"Fetching items from pinterest.com with query '{data['options']['query']}'")

    response = requests.get(URL, params={"source_url": source_url, "data": json.dumps(data)}, headers={})

    assert response.status_code == 200, f"Error {response.status_code} when fetching items"
    resp_data = response.json()
    assert resp_data["resource_response"]["status"] == "success", \
        f"Error {response.json()['resource_response']['status']} when fetching items"

    model = Model(**resp_data)

    logger.info(f"Got {len(model.resource_response.data.results)} items")

    return model


def get_items(limit: int = 50, query: str = "people") -> List[ProcessedItem]:
    processed_items = []
    data = _get_data(query=query)

    while len(processed_items) < limit:
        model = _get_model(data)
        for item in model.resource_response.data.results:
            processed_items.append(ProcessedItem(id=item.id, title=item.title, media=item.images.orig.url))
        data = _get_data(options=model.resource.options)

    logger.info(f"Got {len(processed_items)} items")

    return processed_items
