from flask import Blueprint

pdfs_blueprint = Blueprint('pdfs', __name__)

from . import views