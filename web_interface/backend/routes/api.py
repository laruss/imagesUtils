import flask
from flask import Blueprint

from web_interface.backend.routes.cloud import cloud_bp
from web_interface.backend.routes.description import description_bp
from web_interface.backend.routes.download import download_bp
from web_interface.backend.routes.images import images_bp
from web_interface.backend.routes.optimize import optimize_bp
from web_interface.backend.routes.settings import settings_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

blueprints = [
    settings_bp,
    images_bp,
    download_bp,
    optimize_bp,
    description_bp,
    cloud_bp
]

[api_bp.register_blueprint(bp) for bp in blueprints]


@api_bp.route('/', methods=['GET'])
def index():
    return flask.jsonify({'success': True, 'data': 'api'})
