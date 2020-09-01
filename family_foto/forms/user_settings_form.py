from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField


class UserSettingsForm(FlaskForm):
    """
    Form of user settings.
    """
    share_with = SelectMultipleField('ShareWith', choices=[])
    submit = SubmitField('Save changes')