import flask
from flask import Blueprint

from web_interface.backend.controllers.settings import get_settings
from web_interface.backend.controllers import description as controller

description_bp = Blueprint('description', __name__, url_prefix='/description')


@description_bp.route('/', methods=['GET'])
def describe():
    settings_data = get_settings()

    method = flask.request.args.get('method') or "describe"
    gpt_model = flask.request.args.get('gptModel') or settings_data['description']['gpt_model']
    used_gpt = flask.request.args.get('usedGpt') or settings_data['description']['used_gpt']

    try:
        result = controller.describe(method=method, gpt_model=gpt_model, used_gpt=used_gpt)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200
