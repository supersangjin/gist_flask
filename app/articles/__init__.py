from flask import Blueprint

articles_blueprint = Blueprint('articles', __name__)

from . import views