from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article, User
from app import db
from flask_login import login_required

utils_blueprint = Blueprint('utils', __name__)

@utils_blueprint.route('/search')
def search():
  query = request.args.get('query')
  results = Article.query.all()
  #results = Article.query.whoosh_search(query).all()
  results = Article.query.filter(Article.article_title.ilike('%{}%'.format(query))).all()
  return render_template('utils/search.html', articles=results)