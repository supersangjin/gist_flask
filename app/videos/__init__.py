from flask import Blueprint

videos_blueprint = Blueprint('videos', __name__)

from . import views