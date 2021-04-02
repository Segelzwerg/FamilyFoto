from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class ResetLinkForm(FlaskForm):
    """
    Form that contains only a submit button.
    """
    username = HiddenField('username')
    submit = SubmitField('Reset password')
