from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    """
    Form for registering an user.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email])
    password = PasswordField('Password', validators=[DataRequired()])
    password_control = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_on_submit(self):
        return super().validate_on_submit() and self.password.data == self.password_control.data
