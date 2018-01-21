from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app.models import Article, User, Comment
from app import db
from flask_login import login_required
from .forms import WriteArticleForm, EditArticleForm
from flask_login import current_user
from flask_paginate import Pagination, get_page_parameter
from . import articles_blueprint
import jsonpickle

ARTICLE_LIMIT = 4
PER_PAGE = 3

@articles_blueprint.route('/article', defaults={'page': 1, 'sort':'view'})
@articles_blueprint.route('/article/<sort>', defaults={'page': 1})
@articles_blueprint.route('/article/<sort>/<int:page>')
def index(page, sort):
    if sort == "new":
        article_with_user = db.session.query(Article, User).join(User).order_by(
            Article.article_creDate.desc()).paginate(per_page=PER_PAGE, page=page)
    elif sort == "view":
        article_with_user = db.session.query(Article, User).join(User).order_by(Article.article_hit.desc()).paginate(
            per_page=PER_PAGE, page=page)
    elif sort == "answer":
        article_with_user = db.session.query(Article, User).join(User).order_by(
            Article.article_comment_num.desc()).paginate(per_page=PER_PAGE, page=page)
    else:  # just go to vote if other case
        article_with_user = db.session.query(Article, User).join(User).order_by(Article.article_like.desc()).paginate(
            per_page=PER_PAGE, page=page)
    return render_template('articles/list.html', articles=article_with_user, sort=sort)


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


@articles_blueprint.route('/article/<article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to edit articles.', 'error')
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


@articles_blueprint.route('/article/<article_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_article(article_id):
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to delete articles.', 'error')
        return redirect(url_for('articles.index'))
    article = db.session.query(Article).filter(Article.id == article_id).first()
    if user.id != article.user_id:
        flash('You do not have the authority to delete this article.', 'error')
        return redirect(url_for('articles.index'))
    db.session.delete(article)
    db.session.commit()
    flash('Article, {}, delete success!'.format(article.article_title), 'success')
    return redirect(url_for('articles.index'))


@articles_blueprint.route('/article/<article_id>/detail')
def article_details(article_id):
    article_with_user = db.session.query(Article, User).join(User).filter(Article.id == article_id).first()
    if article_with_user is not None:
        visited = session.get('article' + article_id, '')
        if visited == '':  # 이번 세션동안 방문한적 없음
            session['article' + article_id] = "visited"
            article_with_user.Article.article_hit += 1
            db.session.commit()
        return render_template('articles/article_detail.html', article=article_with_user, current_user_id=current_user.id)
    else:
        flash('Error! Article does not exist.', 'error')
    return redirect(url_for('articles.index'))


@articles_blueprint.route('/article/<article_id>/comment/add', methods=['GET', 'POST'])
def add_comment(article_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        comment_context = data['comment_context']

        # new comment added
        new_comment = Comment(comment_context, current_user.id)
        new_comment.set_article_id(article_id)

        # article comment num += 1
        article = db.session.query(Article).filter(Article.id == article_id).first()
        article.add_comment()

        db.session.add(new_comment)
        db.session.commit()

    all_comments = db.session.query(Comment).filter(Comment.article_id == article_id)
    result_list = []
    for comment in all_comments:
        author = db.session.query(User).filter(User.id == comment.user_id).first()
        result_list.append(
            {
                "id": comment.id,
                "comment_context": comment.comment_context,
                "comment_like": comment.comment_like,
                "comment_creDate": comment.comment_creDate,
                "author_id": author.id,
                "author": author.username,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    result_list.reverse()
    return jsonify(result_list)


@articles_blueprint.route('/article/<article_id>/comment/delete', methods=['POST'])
def delete_comment(article_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        comment_id = data['id']
        # delete comment
        comment = db.session.query(Comment).filter(Comment.id == comment_id).first()

        if current_user.id == comment.user_id:
            db.session.delete(comment)
            db.session.commit()

    all_comments = db.session.query(Comment).filter(Comment.article_id == article_id)
    result_list = []
    for comment in all_comments:
        author = db.session.query(User).filter(User.id == comment.user_id).first()
        result_list.append(
            {
                "id": comment.id,
                "comment_context": comment.comment_context,
                "comment_like": comment.comment_like,
                "comment_creDate": comment.comment_creDate,
                "author": author.username,
                "author_id": author.id,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    result_list.reverse()
    return jsonify(result_list)




# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')
