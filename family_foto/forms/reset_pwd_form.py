from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class ResetPasswordForm(FlaskForm):
    """
    Form for setting a new password.
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password_control = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Change password')
