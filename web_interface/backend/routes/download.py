import flask
from flask import Blueprint

from web_interface.backend.controllers.settings import get_settings
from web_interface.backend.controllers import download as controller

download_bp = Blueprint('download', __name__, url_prefix='/download')


@download_bp.route('/', methods=['GET'])
def download():
    settings_data = get_settings()
    items = int(flask.request.args.get('limit')) or settings_data['download']['images_limit']
    source = flask.request.args.get('source') or 'pinterest'
    prompt = flask.request.args.get('prompt') or settings_data['download']['prompt']

    try:
        controller.download(items=items, source=source, prompt=prompt)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify({'success': True, 'downloaded': items, 'source': source, 'prompt': prompt}), 200
