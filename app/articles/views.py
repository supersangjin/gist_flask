from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article, User
from app import db
from flask_login import login_required
from .forms import WriteArticleForm
from flask_login import current_user

articles_blueprint = Blueprint('articles', __name__)

ARTICLE_LIMIT = 4

@articles_blueprint.route('/')
@articles_blueprint.route('/article')
def index():
    all_articles = Article.query.limit(ARTICLE_LIMIT).all()
    return render_template('articles/articles.html', articles=all_articles)


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


@articles_blueprint.route('/article/<article_id>')
def article_details(article_id):
    article_with_user = db.session.query(Article, User).join(User).filter(Article.id == article_id).first()
    if article_with_user is not None:
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
