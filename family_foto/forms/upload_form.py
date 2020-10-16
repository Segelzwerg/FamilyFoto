from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, MultipleFileField


class UploadForm(FlaskForm):
    """
    Data form of upload mask.
    """
    file = MultipleFileField('File', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
    submit = SubmitField('Upload')
