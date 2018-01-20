from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class WriteArticleForm(FlaskForm):
    article_title = StringField('Article Title', validators=[DataRequired()])
    article_context = StringField('Article Context', validators=[DataRequired()])
    article_category = SelectField(
        'Category',
        choices=[(1, 'Fiction'), (2, 'Memoir'), (3, 'Science'), (4, 'History'), (5, 'Art')],
        coerce=int
    )


class EditArticleForm(FlaskForm):
    article_title = StringField('Article Title', validators=[DataRequired()])
    article_context = StringField('Article Context', validators=[DataRequired()])
    article_category = SelectField(
        'Category',
        choices=[(1, 'Fiction'), (2, 'Memoir'), (3, 'Science'), (4, 'History'), (5, 'Art')],
        coerce=int
    )
