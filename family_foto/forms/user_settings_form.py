from flask_wtf import FlaskForm
from wtforms import SubmitField

from family_foto.forms.fields.multi_checkbox_field import MultiCheckboxField


class UserSettingsForm(FlaskForm):
    """
    Form of user settings.
    """
    share_with = MultiCheckboxField('ShareWith', choices=[])
    submit = SubmitField('Save changes')
