from datetime import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from app import bcrypt

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy import event


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.Binary(60), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_logged_in = db.Column(db.DateTime, nullable=True)
    current_logged_in = db.Column(db.DateTime, nullable=True)
    role = db.Column(db.String, default='user')
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    videos = db.relationship('Video', backref='user', lazy='dynamic')

    def __init__(self, username, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.role = role
        self.username = username
        self.email = email
        self.password = plaintext_password
        self.authenticated = False
        self.email_confirmation_sent_on = email_confirmation_sent_on
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.registered_on = datetime.now()
        self.last_logged_in = None
        self.current_logged_in = datetime.now()
        if self.role == "admin":
            self.email_confirmed = True

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        return bcrypt.check_password_hash(self.password, plaintext_password)

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        """Requires use of Python 3"""
        return str(self.id)

    def __repr__(self):
        return '<User {0}>'.format(self.name)


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String, nullable=False)
    article_context = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_creDate = db.Column(db.DateTime, nullable=True)
    article_hit = db.Column(db.Integer)
    article_like = db.Column(db.Integer)

    def __init__(self, title, context, user_id):
        self.article_title = title
        self.article_context = context
        self.user_id = user_id
        self.article_creDate = datetime.now()
        self.article_hit = 1
        self.article_like = 0

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.article_title, self.user_id)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_context = db.Column(db.String, nullable=False)
    comment_like = db.Column(db.Integer)
    comment_creDate = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdfs.id'))

    def __init__(self, context, user_id):
        self.comment_context = context
        self.comment_like = 0
        self.comment_creDate = datetime.now()
        self.user_id = user_id

    def set_article_id(self, article_id):
        self.article_id = article_id

    def set_video_id(self, video_id):
        self.video_id = video_id

    def set_pdf_id(self, pdf_id):
        self.pdf_id = pdf_id

    def __repr__(self):
        return '<id: {}, context: {}, user_id: {}, article_id: {}>'.format(self.id, self.comment_context, self.user_id, self.article_id)


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    video_title = db.Column(db.String, nullable=False)
    video_description = db.Column(db.String, nullable=False)
    video_filename = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, filename, user_id):
        self.video_title = title
        self.video_description = description
        self.video_filename = filename
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.video_title, self.user_id)


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String, nullable=False)
    question_context = db.Column(db.String, nullable=False)
    question_length = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    answers = db.relationship('Answer', backref='questions', cascade='all, delete', order_by='Answer.id')

    def __init__(self, title, context, user_id):
        self.question_title = title
        self.question_context = context
        self.question_length = 0
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.question_title, self.user_id)


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer_context = db.Column(db.String, nullable=False)

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, context, question_id, user_id):
        self.answer_context = context
        self.question_id = question_id
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, question_id: {}, user_id: {}>'.format(self.id, self.question_id, self.user_id)


class Pdf(db.Model):
    __tablename__ = "pdfs"

    id = db.Column(db.Integer, primary_key=True)
    pdf_title = db.Column(db.String, nullable=False)
    pdf_filename = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pdf_creDate = db.Column(db.DateTime, nullable=True)
    pdf_hit = db.Column(db.Integer)
    pdf_like = db.Column(db.Integer)

    def __init__(self, title, filename, user_id):
        self.pdf_title = title
        self.pdf_filename = filename
        self.user_id = user_id
        self.pdf_creDate = datetime.now()
        self.pdf_hit = 1
        self.pdf_like = 0

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.pdf_title, self.user_id)


def question_answers_append(question, answer, initiator):
    """Update some question values when `Question.answers.append` is called."""
    question.question_length += 1


event.listen(Question.answers, 'append', question_answers_append)
