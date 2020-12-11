from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField


class ApprovalForm(FlaskForm):
    users = SelectMultipleField()
    submit = SubmitField('Approve User(s)')
