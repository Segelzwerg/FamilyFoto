from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class PublicForm(FlaskForm):
    """
    Form to share at the public gallery.
    """
    public = BooleanField(false_values=[False], default=False, render_kw={'value': 'n'})
    submit = SubmitField('Save changes')
