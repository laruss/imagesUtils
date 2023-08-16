import flask
from flask import Blueprint

from web_interface.backend.controllers import settings as controller

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/', methods=['GET'])
def get_settings():
    return flask.jsonify(controller.get_settings())


@settings_bp.route('/', methods=['POST'])
def set_settings():
    data = flask.request.json

    try:
        result = controller.set_settings(data)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200
