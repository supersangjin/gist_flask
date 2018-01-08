from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    """Accepts a room name."""
    room = StringField('Room', validators=[DataRequired()])
