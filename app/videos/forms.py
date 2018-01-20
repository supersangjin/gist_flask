from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class UploadVideoForm(FlaskForm):
    video_title = StringField('Video Title', validators=[DataRequired()])
    video_description = StringField('Video Description', validators=[DataRequired()])
    video_category = SelectField(
        'Category',
        choices=[(1, 'Fiction'), (2, 'Memoir'), (3, 'Science'), (4, 'History'), (5, 'Art')],
        coerce=int
    )
