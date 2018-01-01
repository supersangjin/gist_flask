from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class WriteQuestionForm(FlaskForm):
    question_title = StringField('Question Title', validators=[DataRequired()])
    question_context = StringField('Question Context', validators=[DataRequired()])

class WriteAnswerForm(FlaskForm):
    answer_context = StringField('Answer Context', validators=[DataRequired()])

