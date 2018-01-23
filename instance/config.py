import os

# grab the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

# Update later by using a random number generator and moving
# the actual key outside of the source code under version control
SECRET_KEY = b'\x90zz\xdbXF\x8b\xbb\x1a\xbf\x86\x0fT\xe1\x12\xd3\x99\x17\x92}\xe1\xb1\xe9\xf7'
DEBUG = True

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://gist_admin:kaistgist@localhost/gist'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# CSRF protection
WTF_CSRF_ENABLED = True

# Bcrypt algorithm hashing rounds
BCRYPT_LOG_ROUNDS = 15

# Email
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'gistkaist@gmail.com'
MAIL_PASSWORD = 'kaistgist'
MAIL_DEFAULT_SENDER = 'gistkaist@gmail.com'

# Markdown Editor
SIMPLEMDE_JS_IIFE = True
SIMPLEMDE_USE_CDN = True

UPLOAD_FOLDER = 'app/static/vid'
ALLOWED_EXTENSIONS = ['mp4', 'avi']
UPLOAD_FOLDER_PDF = 'app/static/pdf'
ALLOWED_EXTENSIONS_PDF = ['pdf']
