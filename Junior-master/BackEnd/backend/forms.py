from flask_wtf import FlaskForm
from flask_wtf.file import file_allowed,FileField,file_required
from wtforms import SubmitField,SelectField
from wtforms.validators import DataRequired


class ImageForm(FlaskForm):
    image=FileField('Choose File',validators=[file_required(),file_allowed(['pdf','doc','docx','jpg'])])
    language=SelectField('Language',default='English',choices=[('English','English'),('France','France'),('Arabic','Arabic')])
    submit=SubmitField('Secure')
    
