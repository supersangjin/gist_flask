from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class UploadPdfForm(FlaskForm):
    pdf_title = StringField('Pdf Title', validators=[DataRequired()])
    pdf_description = StringField('Pdf Description', validators=[DataRequired()])
    pdf_category = SelectField(
        'Category',
        choices=[(1, 'Fiction'), (2, 'Memoir'), (3, 'Science'), (4, 'History'), (5, 'Art')],
        coerce=int
    )
