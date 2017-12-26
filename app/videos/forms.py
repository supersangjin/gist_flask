from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UploadVideoForm(FlaskForm):
    video_title = StringField('Video Title', validators=[DataRequired()])
    video_description = StringField('Video Description', validators=[DataRequired()])