import flask
from flask import Blueprint

from web_interface.backend.controllers import images as controller
from web_interface.backend.helpers.utils import success_response, not_found_response, error_handler

images_bp = Blueprint('images', __name__, url_prefix='/images')


@images_bp.route('/', methods=['GET'])
@error_handler
def list_images():
    return success_response(controller.get_images_list())


@images_bp.route('/<image_id>', methods=['GET'])
@error_handler
def get_image(image_id):
    return controller.get_image(image_id)


@images_bp.route('/<image_id>', methods=['DELETE'])
@error_handler
def delete_image(image_id):
    controller.delete_image(image_id)

    return success_response()


@images_bp.route('/<image_id>/data', methods=['GET'])
@error_handler
def get_image_data(image_id):
    return success_response(controller.get_image_data(image_id))


@images_bp.route('/data/schema', methods=['GET'])
@error_handler
def get_image_data_schema():
    return success_response(controller.get_image_data_schema())


@images_bp.route('/<image_id>/data', methods=['POST'])
@error_handler
def set_image_data(image_id):
    return success_response(controller.set_image_data(image_id, flask.request.json))


@images_bp.route('/<image_id>/description', methods=['PUT'])
@error_handler
def generate_image_description(image_id):
    controller.generate_image_description(image_id)

    return success_response()


@images_bp.route('/<image_id>/gpt', methods=['PUT'])
@error_handler
def process_by_gpt(image_id):
    controller.process_by_gpt(image_id)

    return success_response()


@images_bp.route('/<image_id>/gpt/json', methods=['PUT'])
@error_handler
def gpt2json(image_id):
    controller.gpt2json(image_id)

    return success_response()


@images_bp.route('/<image_id>/webp', methods=['PUT'])
@error_handler
def to_webp(image_id):
    controller.to_webp(image_id)

    return success_response()


@images_bp.route('/<image_id>/optimize', methods=['PUT'])
@error_handler
def optimize(image_id):
    controller.optimize_image(image_id)

    return success_response()


