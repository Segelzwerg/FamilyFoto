from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class PublicForm(FlaskForm):
    """
    Form to share at the public gallery.
    """
    public = BooleanField()
    submit = SubmitField('Save changes')
