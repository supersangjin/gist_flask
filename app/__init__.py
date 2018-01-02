from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from flask_misaka import Misaka

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

from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

# blueprints
from app.users.views import users_blueprint
from app.articles.views import articles_blueprint
from app.videos.views import videos_blueprint
from app.forums.views import forums_blueprint
from app.searchs.views import searchs_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(articles_blueprint)
app.register_blueprint(videos_blueprint)
app.register_blueprint(forums_blueprint)
app.register_blueprint(searchs_blueprint)

# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

