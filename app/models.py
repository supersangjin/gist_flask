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
    thumbnail = db.Column(db.String, default=None, nullable=True)
    description = db.Column(db.String, default=None, nullable=True)
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
        self.thumbnail = "user-default.png"
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

    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail

    def set_description(self, description):
        self.description = description

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
    article_comment_num = db.Column(db.Integer)

    def __init__(self, title, context, user_id):
        self.article_title = title
        self.article_context = context
        self.user_id = user_id
        self.article_creDate = datetime.now()
        self.article_hit = 1
        self.article_like = 0
        self.article_comment_num = 0

    def add_comment(self):
        self.article_comment_num += 1

    def delete_comment(self):
        if self.article_comment_num > 0:
            self.article_comment_num -= 1

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.article_title, self.user_id)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment_context = db.Column(db.String, nullable=False)
    comment_like = db.Column(db.Integer)
    comment_creDate = db.Column(db.DateTime, nullable=False)
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


class Chat(db.Model):
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True)
    chat_context = db.Column(db.String, nullable=False)
    chat_creDate = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, context, user_id):
        self.chat_context = context
        self.chat_creDate = datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, context: {}, user_id: {}>'.format(self.id, self.chat_context, self.user_id)


class Video(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String, nullable=False)
    video_title = db.Column(db.String, nullable=False)
    video_description = db.Column(db.String, nullable=True)
    video_duration = db.Column(db.Float, nullable=False)
    video_thumbnail = db.Column(db.String, nullable=False)
    video_html = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    video_creDate = db.Column(db.DateTime, nullable=True)
    video_view = db.Column(db.Integer)
    video_like = db.Column(db.Integer)

    def __init__(self, video_id, title, description, duration, thumbnail, html,  user_id, book_id):
        self.video_id = video_id
        self.video_title = title
        self.video_description = description
        self.video_duration = duration
        self.video_thumbnail = thumbnail
        self.video_html = html
        self.user_id = user_id
        self.book_id = book_id
        self.video_creDate = datetime.now()
        self.video_view = 1
        self.video_like = 0

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.video_title, self.user_id)


class Pdf(db.Model):
    __tablename__ = "pdfs"

    id = db.Column(db.Integer, primary_key=True)
    pdf_title = db.Column(db.String, nullable=False)
    pdf_description = db.Column(db.String, nullable=False)
    pdf_filename = db.Column(db.String, default=None, nullable=True)
    pdf_thumbnail = db.Column(db.String, default=None, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    pdf_creDate = db.Column(db.DateTime, nullable=True)
    pdf_hit = db.Column(db.Integer)
    pdf_like = db.Column(db.Integer)

    pdf_comment_num = db.Column(db.Integer)
    
    def __init__(self, title, description, filename, thumbnail, user_id, book_id):
        self.pdf_title = title
        self.pdf_description = description
        self.pdf_filename = filename
        self.pdf_thumbnail = thumbnail
        self.user_id = user_id
        self.book_id = book_id
        self.pdf_creDate = datetime.now()
        self.pdf_hit = 1
        self.pdf_like = 0
        self.pdf_comment_num = 0

    def add_comment(self):
        self.pdf_comment_num += 1

    def delete_comment(self):
        if self.pdf_comment_num > 0:
            self.pdf_comment_num -= 1

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}, category_id: {}>'.format(self.id, self.pdf_title, self.user_id, self.category_id)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    category_icon = db.Column(db.String, nullable=False)

    books = db.relationship('Book', backref='category', lazy='dynamic')

    def __init__(self, name, icon):
        self.category_name = name
        self.category_icon = icon

    def __repr__(self):
        return '<id: {}, name: {}>'.format(self.id, self.category_name)


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    thumbnail = db.Column(db.String, default=None, nullable=True)
    description = db.Column(db.String, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __init__(self, isbn, title, author, thumbnail, description, category_id):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.thumbnail = thumbnail
        self.description = description
        self.category_id = category_id

    def __repr__(self):
        return '<id: {}, name: {}>'.format(self.id, self.book_title)

