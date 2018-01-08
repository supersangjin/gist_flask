from flask import render_template, request, redirect, url_for, flash
from app.models import Article, User
from app import db
from flask_login import login_required
from .forms import WriteArticleForm, EditArticleForm
from flask_login import current_user
from flask_paginate import Pagination, get_page_parameter
from . import articles_blueprint


ARTICLE_LIMIT = 4
PER_PAGE = 4
"""
@articles_blueprint.route('/')
def root():
    all_articles = Article.query.limit(ARTICLE_LIMIT).all()
    return render_template('articles/articles.html', articles=all_articles)
    """


@articles_blueprint.route('/article/', defaults={'page': 1})
@articles_blueprint.route('/article/<int:page>')
def index(page):
    all_articles = Article.query.limit(ARTICLE_LIMIT).all()

    articles = Article.query.paginate(per_page=PER_PAGE, page=page)

    return render_template('articles/articles.html', articles=articles)


@articles_blueprint.route('/article/add', methods=['GET', 'POST'])
@login_required
def write_article():
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to write articles.', 'error')
        return redirect(url_for('articles.index'))
    form = WriteArticleForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_article = Article(form.article_title.data, form.article_context.data, user.id)
            db.session.add(new_article)
            db.session.commit()
            flash('New Article, {}, added!'.format(new_article.article_title), 'success')
            article_with_user = db.session.query(Article, User).join(User).filter(Article.id == new_article.id).first()
            return render_template('articles/article_detail.html', article=article_with_user)
    return render_template('articles/write_article.html', form=form)


@articles_blueprint.route('/article/edit/<article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to edit articles.', 'error') # 글 작성 후 이메일 주소 바꿨을 수도 있으니까
        return redirect(url_for('articles.index'))
    article = db.session.query(Article).filter(Article.id == article_id).first()
    if user.id != article.user_id:
        flash('You do not have the authority to edit this article.', 'error')
        return redirect(url_for('articles.index'))
    form = EditArticleForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            article.article_title = form.article_title.data
            article.article_context = form.article_context.data
            db.session.commit()
            flash('Article, {}, edit success!'.format(article.article_title), 'success')
            article_with_user = db.session.query(Article, User).join(User).filter(Article.id == article.id).first()
            return render_template('articles/article_detail.html', article=article_with_user)
    return render_template('articles/edit_article.html', form=form, article=article)


@articles_blueprint.route('/article/delete/<article_id>', methods=['GET', 'POST'])
@login_required
def delete_article(article_id):
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to delete articles.', 'error') # 글 작성 후 이메일 주소 바꿨을 수도 있으니까
        return redirect(url_for('articles.index'))
    article = db.session.query(Article).filter(Article.id == article_id).first()
    if user.id != article.user_id:
        flash('You do not have the authority to delete this article.', 'error')
        return redirect(url_for('articles.index'))
    db.session.delete(article)
    db.session.commit()
    flash('Article, {}, delete success!'.format(article.article_title), 'success')
    return redirect(url_for('articles.index'))


@articles_blueprint.route('/article/detail/<article_id>')
def article_details(article_id):
    article_with_user = db.session.query(Article, User).join(User).filter(Article.id == article_id).first()
    if article_with_user is not None:
        article_with_user.Article.article_hit += 1
        db.session.commit()
        return render_template('articles/article_detail.html', article=article_with_user)
    else:
        flash('Error! Article does not exist.', 'error')
    return redirect(url_for('articles.index'))


# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')
