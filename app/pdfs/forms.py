from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class UploadPdfForm(FlaskForm):
    pdf_title = StringField('Pdf Title', validators=[DataRequired()])
    pdf_description = StringField('Pdf Description', validators=[DataRequired()])
    pdf_isbn = StringField('ISBN10', validators=[DataRequired()])
