from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    """Accepts a room name."""
    name = StringField('Name', validators=[DataRequired()])
    room = StringField('Room', validators=[DataRequired()])
