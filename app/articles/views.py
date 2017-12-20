from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Article
from app import db
from flask_login import login_required
from .forms import WriteArticleForm
from flask_login import current_user

articles_blueprint = Blueprint('articles', __name__)


@articles_blueprint.route('/')
def index():
    all_articles = Article.query.all()
    return render_template('articles.html', articles=all_articles)


@articles_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def write_article():
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to write articles.', 'error')
        return redirect(url_for('articles.index'))
    form = WriteArticleForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_article = Article(form.article_title.data, form.article_context.data)
            db.session.add(new_article)
            db.session.commit()
            flash('New Article, {}, added!'.format(new_article.article_title), 'success')
            return redirect(url_for('articles.index'))

    return render_template('write_article.html', form=form)


# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')