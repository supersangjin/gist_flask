from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify
from app.models import Article, User, Video, Category, Pdf, Book
from . import utils_blueprint
from app import db
from flask_login import login_required

ARTICLE_LIMIT = 4


@utils_blueprint.route('/')
def index():
    categories = db.session.query(Category).all()
    videos_join = db.session.query(Video, User, Book, Category)\
        .join(User)\
        .join(Book)\
        .join(Category)\
        .limit(ARTICLE_LIMIT)
    pdfs_join = db.session.query(Pdf, User, Book, Category)\
        .join(User)\
        .join(Book)\
        .join(Category)\
        .limit(ARTICLE_LIMIT)

    if videos_join is not None and pdfs_join is not None:
        return render_template('utils/index.html', pdfs=pdfs_join, videos=videos_join, categories=categories)
    else:
        flash('Error! Video does not exist.', 'error')  # TODO: error handling
    return redirect(url_for('utils.index'))


@utils_blueprint.route('/search')
def search():
    query = request.args.get('query')
    # results = Article.query.whoosh_search(query).all()
    books = db.session.query(Book).filter(Book.title.ilike('%{}%'.format(query))).all()
    return render_template('utils/search.html', books=books)


@utils_blueprint.route('/search_filter', methods=['POST'])
def searchFilter():
    data = request.form.to_dict()
    all_books = db.session.query(Book).filter(Book.title.ilike('%{}%'.format(data["term"]))).all()
    result_list = []
    for book in all_books:
        result_list.append(
            {
                "id": book.id,
                "title": book.title,
                "authors": book.author,
                "thumbnail": book.thumbnail
            }
        )
    return jsonify(result_list)
