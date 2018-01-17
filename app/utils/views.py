from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article, User, Video
from . import utils_blueprint
from app import db
from flask_login import login_required

ARTICLE_LIMIT = 4

@utils_blueprint.route('/')
def index():
	articles = Article.query.limit(ARTICLE_LIMIT).all()
	videos = Video.query.limit(ARTICLE_LIMIT).all()

	return render_template('utils/index.html', articles=articles, videos=videos)

@utils_blueprint.route('/search')
def search():
  query = request.args.get('query')
  #results = Article.query.whoosh_search(query).all()
  results = Article.query.filter(Article.article_title.ilike('%{}%'.format(query))).all()
  return render_template('utils/search.html', articles=results)