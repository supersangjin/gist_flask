from flask import Blueprint

utils_blueprint = Blueprint('utils', __name__)

from . import views