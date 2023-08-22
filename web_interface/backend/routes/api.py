from flask import Blueprint

from optimize.settings import Methods as OptimizeMethods
from description.settings import Methods as DescriptionMethods
from cloud.settings import Methods as CloudMethods
from web_interface.backend.helpers.utils import success_response
from web_interface.backend.routes.images import images_bp
from web_interface.backend.routes.settings import settings_bp
from web_interface.backend.controllers import api as controller

api_bp = Blueprint("api", __name__, url_prefix="/api")

blueprints = [settings_bp, images_bp]

[api_bp.register_blueprint(bp) for bp in blueprints]


@api_bp.route("/download", methods=["POST"])
def download_images():
    message = controller.download_images()

    return success_response(message=message)


@api_bp.route("/optimize", methods=["POST"])
def optimize_images():
    message = controller.optimize_images()

    return success_response(message=message)


@api_bp.route("/optimize/webp", methods=["POST"])
def optimize_images_to_webp():
    message = controller.optimize_images(OptimizeMethods.to_webp)

    return success_response(message=message)


@api_bp.route("/optimize/minimize", methods=["POST"])
def optimize_images_minimize():
    message = controller.optimize_images(OptimizeMethods.minimize)

    return success_response(message=message)


@api_bp.route("/optimize/duplicates", methods=["DELETE"])
def optimize_images_duplicates():
    message = controller.optimize_images(OptimizeMethods.delete_duplicates)

    return success_response(message=message)


@api_bp.route("/description", methods=["POST"])
def describe_images():
    message = controller.describe_images()

    return success_response(message=message)


@api_bp.route("/description/describe", methods=["POST"])
def describe_images_describe():
    message = controller.describe_images(DescriptionMethods.describe)

    return success_response(message=message)


@api_bp.route("/description/delete/nsfw", methods=["POST"])
def describe_images_delete_nsfw():
    message = controller.describe_images(DescriptionMethods.delete_nsfw)

    return success_response(message=message)


@api_bp.route("/description/gpt", methods=["POST"])
def describe_images_gpt():
    message = controller.describe_images(DescriptionMethods.gpt)

    return success_response(message=message)


@api_bp.route("/description/gpt2json", methods=["POST"])
def describe_images_gpt2json():
    message = controller.describe_images(DescriptionMethods.gpt2json)

    return success_response(message=message)


@api_bp.route("/cloud", methods=["POST"])
def cloud_images():
    message = controller.cloud_images()

    return success_response(message=message)


@api_bp.route("/cloud/upload", methods=["POST"])
def cloud_images_upload():
    message = controller.cloud_images(CloudMethods.upload)

    return success_response(message=message)


@api_bp.route("/cloud/download", methods=["POST"])
def cloud_images_download():
    message = controller.cloud_images(CloudMethods.download)

    return success_response(message=message)


@api_bp.route("/", methods=["GET"])
def index():
    return success_response()
