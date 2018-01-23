from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from flask_misaka import Misaka
# from flask_socketio import SocketIO

# config
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('instance.config')

# database
db = SQLAlchemy(app)

# password hashing
bcrypt = Bcrypt(app)

# email
mail = Mail(app)

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Markdpwn Editor
SimpleMDE(app)
md = Misaka(fenced_code=True, tables=True)
md.init_app(app)

# Chat
# socketio = SocketIO()
# socketio.init_app(app)

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

# blueprints
from app.users.views import users_blueprint
from app.articles.views import articles_blueprint
from app.videos.views import videos_blueprint
from app.utils.views import utils_blueprint
from app.chat.views import chat_blueprint
from app.pdfs.views import pdfs_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(articles_blueprint)
app.register_blueprint(videos_blueprint)
app.register_blueprint(utils_blueprint)
app.register_blueprint(chat_blueprint)
app.register_blueprint(pdfs_blueprint)


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403


@app.errorhandler(410)
def page_not_found(e):
    return render_template('error/410.html'), 410


# function for all templates
@app.context_processor
def utility_processor():
	TITLE_LENGTH_LIMIT = 35
	def format_list_title(title):
		if len(title) < TITLE_LENGTH_LIMIT :
			return title
		else :
			return title [:TITLE_LENGTH_LIMIT] + "..."
	return dict(format_list_title = format_list_title)
