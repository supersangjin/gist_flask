from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article, User, Video, Category, Pdf
from . import utils_blueprint
from app import db
from flask_login import login_required

ARTICLE_LIMIT = 4

@utils_blueprint.route('/')
def index():
	categorys = Category.query.all()
	videos_join = db.session.query(Video, User, Category).join(User, Category).limit(ARTICLE_LIMIT)
	pdfs_join = db.session.query(Pdf, User, Category).join(User, Category).limit(ARTICLE_LIMIT)
	
	if videos_join is not None and pdfs_join is not None :
		return render_template('utils/index.html', pdfs=pdfs_join, videos=videos_join, categorys=categorys)
	else :
		flash('Error! Video does not exist.', 'error') # TODO: error handling
	return redirect(url_for('utils.index'))

@utils_blueprint.route('/search')
def search():
  query = request.args.get('query')
  #results = Article.query.whoosh_search(query).all()
  results = Article.query.filter(Article.article_title.ilike('%{}%'.format(query))).all()
  return render_template('utils/search.html', articles=results)