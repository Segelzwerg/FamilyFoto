from wtforms import SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    """
    Field for selecting multiple fields from checkbox list.
    """
    widget = widgets.ListWidget(html_tag='ul', prefix_label=False)
    option_widget = widgets.CheckboxInput()
