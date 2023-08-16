import flask
from flask import Blueprint

from web_interface.backend.controllers import images as controller

images_bp = Blueprint('images', __name__, url_prefix='/images')


@images_bp.route('/', methods=['GET'])
def list_images():
    return flask.jsonify(controller.get_images_list())


@images_bp.route('/<image_id>', methods=['GET'])
def get_image(image_id):
    try:
        return controller.get_image(image_id)
    except Exception as e:
        if isinstance(e, IndexError):
            return flask.jsonify({'error': 'Image not found'}), 404

        return flask.jsonify({'error': str(e)}), 400


@images_bp.route('/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    return flask.jsonify({'success': True})


@images_bp.route('/<image_id>/data', methods=['GET'])
def get_image_data(image_id):
    try:
        result = controller.get_image_data(image_id)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 404

    return flask.jsonify(result)


@images_bp.route('/<image_id>/data', methods=['POST'])
def set_image_data(image_id):
    data = flask.request.json

    try:
        result = controller.set_image_data(image_id, data)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200
