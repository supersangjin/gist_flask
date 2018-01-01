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

    def __init__(self, email, plaintext_password, email_confirmation_sent_on=None, role='user'):
        self.role = role
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

    def __init__(self, title, context, user_id):
        self.article_title = title
        self.article_context = context
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.article_title, self.user_id)


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, context, user_id):
        self.question_title = title
        self.question_context = context
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

"""
class Forum(db.Model):
    __tablename__ = "forums"

    id = db.Column(db.Integer, primary_key=True)
    forum_title = db.Column(db.String, nullable=False)
    forum_content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    answers = db.relationship('Answer', backref='thread',
                            cascade='all,delete',
                            order_by='Post.index',
                            collection_class=ordering_list('index'))

    def __init__(self, title, description, filename, user_id):
        self.video_title = title
        self.video_description = description
        self.video_filename = filename
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.video_title, self.user_id)

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer_content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, description, filename, user_id):
        self.video_title = title
        self.video_description = description
        self.video_filename = filename
        self.user_id = user_id

    def __repr__(self):
        return '<id: {}, title: {}, user_id: {}>'.format(self.id, self.video_title, self.user_id)
"""
"""
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class TimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def readable_date(self, date, format='%H:%M on %-d %B'):
        return date.strftime(format)

class Board(Base):

    #: The human-readable name, e.g. "Python 3"
    name = db.Column(db.String)

    #: The URL-encoded name, e.g. "python-3"
    slug = db.Column(db.String, unique=True)

    #: A short description of what the board contains.
    description = db.Column(db.Text)

    #: The threads associated with this board.
    threads = db.relationship('Thread', cascade='all,delete', backref='board')

    def __unicode__(self):
        return self.name

class Thread(Base, TimestampMixin):
    name = db.Column(db.String(80))

    #: The original author of the thread.
    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    # author = db.relationship('User', backref='threads')

    #: The parent board.
    board_id = db.Column(db.ForeignKey('board.id'), index=True)

    #: An ordered collection of posts
    posts = db.relationship('Post', backref='thread',
                            cascade='all,delete',
                            order_by='Post.index',
                            collection_class=ordering_list('index'))

    #: Length of the threads
    length = db.Column(db.Integer, default=0)

    def __unicode__(self):
        return self.name


class Post(Base, TimestampMixin):
    #: Used to order the post within its :class:`Thread`
    index = db.Column(db.Integer, default=0, index=True)

    #: The post content. The site views expect Markdown by default, but
    #: you can store anything here.
    content = db.Column(db.Text)

    #: The original author of the post.
    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    # author = db.relationship('User', backref='posts')

    #: The parent thread.
    thread_id = db.Column(db.ForeignKey('thread.id'), index=True)


    def __repr__(self):
        return '<Post(%s)>' % self.id

def thread_posts_append(thread, post, initiator):
    thread.length += 1
    thread.updated = datetime.utcnow()

event.listen(Thread.posts, 'append', thread_posts_append)
"""
