import os
from flask import Blueprint, send_from_directory
from werkzeug.wrappers import Response
from typing import Union

# React build folder
react_public_dir = os.path.join(os.getcwd(), "dist/public")
react_blueprint = Blueprint("react", __name__, static_folder=react_public_dir, url_prefix="/")

MISSING_STATIC_ROOT_ERR_MESSAGE = "Unable to resolve react root path"

@react_blueprint.route("/", defaults={"path": ""})
@react_blueprint.route("/<path:path>")
def serve_react_home(path: Union[str, os.PathLike]) -> Response:
    assert react_blueprint.static_folder, MISSING_STATIC_ROOT_ERR_MESSAGE
    return send_from_directory(react_blueprint.static_folder, "index.html")

@react_blueprint.route("/index.bundle.js")
def serve_js_bundle() -> Response:
    assert react_blueprint.static_folder, MISSING_STATIC_ROOT_ERR_MESSAGE
    return send_from_directory(react_blueprint.static_folder, "index.bundle.js")

@react_blueprint.route("/style.css")
def serve_css() -> Response:
    assert react_blueprint.static_folder, MISSING_STATIC_ROOT_ERR_MESSAGE
    return send_from_directory(react_blueprint.static_folder, "style.css")


# Image assets
react_img_assets_dir = os.path.join(os.getcwd(), "dist/assets/img")
img_assets_blueprint = Blueprint("image_assets", __name__, static_folder=react_img_assets_dir, url_prefix="/assets")

@img_assets_blueprint.route("/assets/img/<path:filename>")
def serve_static_images(filename: Union[str, os.PathLike]):
    assert img_assets_blueprint.static_folder, MISSING_STATIC_ROOT_ERR_MESSAGE
    return send_from_directory(img_assets_blueprint.static_folder, filename)
