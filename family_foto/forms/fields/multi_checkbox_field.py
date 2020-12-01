from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput


class MultiCheckboxField(SelectMultipleField):
    """
    Field for selecting multiple fields from checkbox list.
    """
    widget = ListWidget(html_tag='ul', prefix_label=False)
    option_widget = CheckboxInput()
