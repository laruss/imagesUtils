import flask
from flask import Blueprint

from web_interface.backend.controllers import images as controller
from web_interface.backend.controllers.settings import get_settings

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
    try:
        controller.delete_image(image_id)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

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


@images_bp.route('/<image_id>/description', methods=['PUT'])
def generate_image_description(image_id):
    settings_data = get_settings()

    source = flask.request.args.get('source') or settings_data['description']['image_to_text_engine']

    try:
        controller.generate_image_description(image_id, source)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify({"success": True}), 200


@images_bp.route('/<image_id>/gpt', methods=['PUT'])
def process_by_gpt(image_id):
    settings_data = get_settings()

    prompt = flask.request.args.get('prompt') or settings_data['description']['default_prompt']
    model = flask.request.args.get('model') or settings_data['description']['gpt_model']
    used_gpt = flask.request.args.get('usedGpt') or settings_data['description']['used_gpt']

    try:
        result = controller.process_by_gpt(image_id, prompt, model, used_gpt)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200


@images_bp.route('/<image_id>/gpt/json', methods=['PUT'])
def gpt2json(image_id):
    try:
        result = controller.gpt2json(image_id)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200


@images_bp.route('/<image_id>/webp', methods=['PUT'])
def to_webp(image_id):
    quality = flask.request.args.get('quality') or 80
    delete_original = flask.request.args.get('deleteOriginal') or True

    try:
        result = controller.to_webp(image_id, quality, delete_original)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200


@images_bp.route('/<image_id>/optimize', methods=['PUT'])
def optimize(image_id):
    image_final_size_kb = flask.request.args.get('imageFinalSizeKb') or 512

    try:
        result = controller.optimize_image(image_id, image_final_size_kb)
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 400

    return flask.jsonify(result), 200


