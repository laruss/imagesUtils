import functools
import json
from typing import Union

import flask

from core.ProcessedItem import ProcessedItem
from core.utils import read_json_from_file
from web_interface.backend.controllers.images import get_image_model
from web_interface.backend.controllers.settings import get_settings


def _response(
    data: dict, status: int = 200, mimetype: str = "application/json"
) -> flask.Response:
    return flask.Response(json.dumps(data), status=status, mimetype=mimetype)


def not_found_response(data: dict = None) -> flask.Response:
    data = data or {"error": "item not found"}

    return _response(data, status=404)


def success_response(
    data: Union[dict, list] = None, message: str = None
) -> flask.Response:
    data = {"message": message} if message else (data or {"success": True})

    return _response(data)


def get_images_models(*images_ids: str) -> list[ProcessedItem]:
    images_ids = images_ids or read_json_from_file(get_settings().core.data_file).keys()

    return [get_image_model(image_id) for image_id in images_ids]


def error_handler(func):
    @functools.wraps(func)
    def wrapper_error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, IndexError) or isinstance(e, KeyError):
                return not_found_response()
            else:
                raise e

    return wrapper_error_handler
