import flask
from flask import Blueprint

from web_interface.backend.controllers.settings import get_settings
from web_interface.backend.controllers import cloud as controller

cloud_bp = Blueprint('cloud', __name__, url_prefix='/cloud')


@cloud_bp.route('/', methods=['GET'])
def index():
    settings_data = get_settings()

    method = flask.request.args.get('method') or "upload"
    provider = flask.request.args.get('provider') or settings_data['cloud']['provider']

    try:
        controller.cloud(method=method, provider=provider)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify({'success': True, 'method': method, 'provider': provider}), 200
