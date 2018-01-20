from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class WriteArticleForm(FlaskForm):
    article_title = StringField('Article Title', validators=[DataRequired()])
    article_context = StringField('Article Context', validators=[DataRequired()])


class EditArticleForm(FlaskForm):
    article_title = StringField('Article Title', validators=[DataRequired()])
    article_context = StringField('Article Context', validators=[DataRequired()])

