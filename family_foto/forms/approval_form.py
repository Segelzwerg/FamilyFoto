from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField


class ApprovalForm(FlaskForm):
    """
    Form for approval accepting.
    """
    users = SelectMultipleField()
    submit = SubmitField('Approve User(s)')
