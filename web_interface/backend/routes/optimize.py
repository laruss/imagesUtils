import flask
from flask import Blueprint

from web_interface.backend.controllers import optimize as controller

optimize_bp = Blueprint('optimize', __name__, url_prefix='/optimize')


@optimize_bp.route('/', methods=['GET'])
def optimize():
    method = flask.request.args.get('method') or 'to_webp'  # 'to_webp' or 'minimize'

    try:
        controller.optimize(method=method)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify({'success': True, 'method': method}), 200
