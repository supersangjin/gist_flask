from flask import Blueprint

forums_blueprint = Blueprint('forums', __name__)

from . import views