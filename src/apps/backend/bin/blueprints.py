from flask import Blueprint
from bin.react_blueprint import react_blueprint, img_assets_blueprint  # import from separate file

# API blueprint
api_blueprint = Blueprint("api", __name__, url_prefix="/api")
