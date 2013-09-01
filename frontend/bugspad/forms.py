import flask
from flask.ext import wtf
from wtforms import (
        TextField, SelectField, validators, PasswordField,
        TextAreaField, FileField, StringField)
from datetime import time
from datetime import datetime


class LoginForm(wtf.Form):
    """ Form to log in the application. """
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])


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
    return [
        ('foo', 'Foo')
    ]

def get_target_release():
    return [
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('rawhide', 'Rawhide')
    ]

class BugForm(wtf.Form):
    """Form to create/edit a bug."""
    # Basic fields
    product = TextField(
        'Product', [validators.Required()],
        default='Fedora', description=(
            "Bugs are categorised into Products and Components. Select a "
            "Classification to narrow down this list."))
    reporter = TextField('Reporter', default='rtnpro@gmail.com')
    component = SelectField(
            'Component', [validators.Required()],
            choices=get_component_choices(), description=(
                "Components are second-level categories; each belongs to a "
                "particular Product. Select a Product to narrow down "
                "this list."))
    version = SelectField(
        'Version', [validators.Required()], choices=get_fedora_versions())
    severity = SelectField('Severity', choices=[
            ('unspecified', 'Unspecified'),
            ('urgent', 'Urgent'),
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low')
        ]
    )
    hardware = SelectField('Hardware', choices=get_hardware_choices())
    os_choice = SelectField('Os', choices=get_os_choices())
    summary = TextField('Summary', [validators.Required()])
    description_default_text = (
        "Description of problem:\n\n\n"
        "Version-Release number of selected component (if applicable):\n\n\n"
        "How reproducible:\n\n\n"
        "Steps to reproduce:\n1.\n2.\n3.\n\n"
        "Actual results:\n\n\n"
        "Expected results:\n\n\n"
        "Additional info:\n\n"
    )
    description = TextAreaField('Description',
                                    default=description_default_text)
    attachment = FileField('Attachment')
    external_bug_location = SelectField(
        'Location', choices=get_external_bug_location_choices())
    external_bug_bugid = TextField('Bug ID')

    # Advanced fields
    target_release = SelectField('Target Release',
                                     choices=get_target_release())
    status = StringField('Status')
    assignee = TextField('Assignee')
    fedora_review = SelectField('Fedora-Review', choices=[('?','?')])
    release_note = SelectField('Fedora requires release note', choices=[
        ('?','?'),
        ('+','+'),
        ('-','-')
    ])
    need_info = SelectField('Need Info', choices=[
        ('?','?'),
        ('+','+'),
        ('-','-')
    ])
    qa_contact = TextField('QA Contact')
    docs_contact = TextField('Docs Contact')
    cc = TextField('CC')
    alias = TextField('Alias')
    url = TextField('URL')
    whiteboard = TextField('Whiteboard')
    clone_of = TextField('Clone Of')
    environment = TextAreaField('Environment')

