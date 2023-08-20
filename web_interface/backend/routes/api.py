from flask import Blueprint

from web_interface.backend.helpers.utils import success_response
from web_interface.backend.routes.images import images_bp
from web_interface.backend.routes.settings import settings_bp
from web_interface.backend.controllers import api as controller

api_bp = Blueprint('api', __name__, url_prefix='/api')

blueprints = [settings_bp, images_bp]

[api_bp.register_blueprint(bp) for bp in blueprints]


@api_bp.route('/download', methods=['POST'])
def download_images():
    message = controller.download_images()

    return success_response(message=message)


@api_bp.route('/optimize', methods=['POST'])
def optimize_images():
    message = controller.optimize_images()

    return success_response(message=message)


@api_bp.route('/description', methods=['POST'])
def describe_images():
    message = controller.describe_images()

    return success_response(message=message)


@api_bp.route('/cloud', methods=['POST'])
def cloud_images():
    message = controller.cloud_images()

    return success_response(message=message)


@api_bp.route('/', methods=['GET'])
def index():
    return success_response()
