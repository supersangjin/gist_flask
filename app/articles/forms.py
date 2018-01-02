from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class WriteArticleForm(FlaskForm):
    article_title = StringField('Article Title', validators=[DataRequired()])
    article_context = StringField('Article Context', validators=[DataRequired()])
