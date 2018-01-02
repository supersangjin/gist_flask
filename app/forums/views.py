from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.models import Question, Answer, User
from app import db
from flask_login import login_required
from .forms import *
from flask_login import current_user

forums_blueprint = Blueprint('forums', __name__)


@forums_blueprint.route('/forum')
def index():
    all_questions = Question.query.all() # TODO: partial request
    return render_template('forums/forums.html', questions=all_questions)


@forums_blueprint.route('/forum/add', methods=['GET', 'POST'])
@login_required
def write_question():
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to write questions.', 'error')
        return redirect(url_for('forums.index'))
    form = WriteQuestionForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_question = Question(form.question_title.data, form.question_context.data, user.id)
            db.session.add(new_question)
            db.session.commit()
            flash('New Question, {}, added!'.format(new_question.question_title), 'success')
            question_with_user = db.session.query(Question, User).join(User).filter(Question.id == new_question.id).first()
            return render_template('forum/question_detail.html', question=question_with_user)
    return render_template('forums/write_question.html', form=form)


@forums_blueprint.route('/forum/<question_id>')
def question_details(question_id):

    try:
        question = Question.query.filter(Question.id == question_id).one()
    except:
        flash('Error! Question does not exist.', 'error')
        return redirect(url_for('forums.index'))

    question_with_user = db.session.query(Question, User).join(User).filter(Question.id == question_id).first()
    answer_with_question = db.session.query(Answer, User).join(User).filter(Answer.question_id == question_id).all()
    if question_with_user is not None:
        return render_template('forums/question_detail.html', question=question_with_user, answers=answer_with_question)
    else:
        flash('Error! Question does not exist.', 'error')
    return redirect(url_for('forums.index'))

@forums_blueprint.route('/forum/<question_id>/answer', methods=['GET', 'POST'])
@login_required
def write_answer(question_id):
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to write answers.', 'error')
        return redirect(url_for('forums.index'))

    try:
        question = Question.query.filter(Question.id == question_id).one()
    except:
        flash('Error! Question does not exist.', 'error')
        return redirect(url_for('forums.index'))

    form = WriteAnswerForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_answer = Answer(form.answer_context.data, question_id, user.id)
            question.answers.append(new_answer)
            db.session.commit()
            flash('New Answer, {}, added!'.format(new_answer.id), 'success')
            question_with_user = db.session.query(Question, User).join(User).filter(Question.id == question_id).first()
            return render_template('forum/question_detail.html', question=question_with_user)
    return render_template('forums/write_answer.html', question_id=question_id, form=form)


# helper functions
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')
