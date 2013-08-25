import flask
from flask.ext import wtf
from datetime import time
from datetime import datetime

from wtforms import ValidationError

class LoginForm(wtf.Form):
    """ Form to log in the application. """
    username = wtf.TextField('Username', [wtf.validators.Required()])
    password = wtf.PasswordField('Password', [wtf.validators.Required()])


def get_component_choices():
    return [
        ('a', 'A'),
        ('b', 'B')
    ]


def get_fedora_versions():
    return [
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('rawhide', 'Rawhide')
    ]


def get_hardware_choices():
    return [('x86_64', 'x86_64')]


def get_os_choices():
    return [('Linux', 'Linux')]


def get_external_bug_location_choices():
    return []


class BugForm(wtf.Form):
    """For to create/edit a bug."""
    # Basic fields
    product = wtf.TextField(
        'Product', [wtf.validators.Required()],
        default='Fedora', description=(
            "Bugs are categorised into Products and Components. Select a "
            "Classification to narrow down this list."))
    reporter = wtf.TextField('Reporter', default='rtnpro@gmail.com')
    component = wtf.SelectField(
            'Component', [wtf.validators.Required()],
            choices=get_component_choices(), description=(
                "Components are second-level categories; each belongs to a "
                "particular Product. Select a Product to narrow down "
                "this list."))
    version = wtf.SelectField(
        'Version', [wtf.validators.Required()], choices=get_fedora_versions())
    severity = wtf.SelectField('Severity', choices=[
            ('unspecified', 'Unspecified'),
            ('urgent', 'Urgent'),
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low')
        ]
    )
    hardware = wtf.SelectField('Hardware', choices=get_hardware_choices())
    os_choice = wtf.SelectField('Os', choices=get_os_choices())
    summary = wtf.TextField('Summary', [wtf.validators.Required()])
    description_default_text = (
        "Description of problem:\n\n\n"
        "Version-Release number of selected component (if applicable):\n\n\n"
        "How reproducible:\n\n\n"
        "Steps to reproduce:\n1.\n2.\n3.\n\n"
        "Actual results:\n\n\n"
        "Expected results:\n\n\n"
        "Additional info:\n\n"
    )
    description = wtf.TextAreaField('Description',
                                    default=description_default_text)
    attachment = wtf.FileField('Attachment')
    external_bug_location = wtf.SelectField(
        'Location', choices=get_external_bug_location_choices())
    external_bug_bugid = wtf.TextField('Bug ID')


    # Advanced fields
