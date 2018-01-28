from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import DataRequired


class UploadVideoForm(FlaskForm):
    id = StringField('id', validators=[DataRequired()])
    title = StringField('Video Title', validators=[DataRequired()])
    description = StringField('Video Description', validators=[DataRequired()])
    isbn = StringField('ISBN10', validators=[DataRequired()])
    duration = StringField('duration', validators=[DataRequired()])
    thumbnail = StringField('thumbnail', validators=[DataRequired()])
    html = StringField('html', validators=[DataRequired()])
