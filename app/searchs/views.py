from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article, User
from app import db
from flask_login import login_required

searchs_blueprint = Blueprint('searchs', __name__)

@searchs_blueprint.route('/search')
def search_results():
  query = request.args.get('query')
  results = Article.query.all()
  #results = Article.query.whoosh_search(query).all()
  results = Article.query.filter(Article.article_title.ilike('%{}%'.format(query))).all()
  return render_template('search_results.html', articles=results)