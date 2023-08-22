import json

import flask
from flask import Blueprint

from web_interface.backend.controllers import settings as controller
from web_interface.backend.helpers.utils import success_response

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/', methods=['GET'])
def get_settings():
    return success_response(controller.get_settings(as_data=True))


@settings_bp.route('/schema', methods=['GET'])
def get_settings_schema():
    return success_response(controller.get_settings_schema())


@settings_bp.route('/', methods=['POST'])
def set_settings():
    controller.set_settings(flask.request.json)
    return success_response(message="Settings updated successfully")


@settings_bp.route('/', methods=['DELETE'])
def reset_settings():
    controller.reset_settings()
    return success_response(message="Settings reset successfully")
