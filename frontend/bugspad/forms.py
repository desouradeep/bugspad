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
        ('1', 'Test'),
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
    return [
        ('unspecified','Unspecified'),
        ('all','All'),
        ('x86_64','x86_64'),
        ('aarch64','aarch64'),
        ('alpha','alpha'),
        ('alphaev6','alphaev6'),
        ('am33','am33'),
        ('arm','arm'),
        ('athlon','athlon'),
        ('i386','i386'),
        ('i586','i586'),
        ('i686','i686'),
        ('ia32e','ia32e'),
        ('ia64','ia64'),
        ('mips32','mips32'),
        ('mips64','mips64'),
        ('noarch','noarch'),
        ('other','other'),
        ('parisc11','parisc11'),
        ('powerpc','powerpc'),
        ('ppc','ppc'),
        ('ppc64','ppc64'),
        ('s390','s390'),
        ('s390x','s390x'),
        ('sparc','sparc'),
        ('sparc64','sparc64'),
        ('sparcv9','sparcv9'),
        ('synth','synth'),
        ('v850','v850')
    ]


def get_os_choices():
    return [
        ('Unspecified','Unspecified'),
        ('All','All'),
        ('Linux','Linux'),
        ('FreeBSD','FreeBSD'),
        ('Solaris','Solaris'),
        ('Mac OS','Mac OS'),
        ('Windows','Windows'),
        ('Other','Other'),
    ]

def get_severity():
    return [
        ('unspecified', 'Unspecified'),
        ('urgent', 'Urgent'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]



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
    user = TextField('Reporter', default='rtnpro@gmail.com')
    component_id = SelectField(
            'Component', [validators.Required()],
            choices=get_component_choices(), description=(
                "Components are second-level categories; each belongs to a "
                "particular Product. Select a Product to narrow down "
                "this list."))
    version = SelectField(
        'Version', [validators.Required()], choices=get_fedora_versions())
    severity = wtf.SelectField('Severity', choices=get_severity())
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

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', '')
        reporter = kwargs.pop('reporter', '')
        super(BugForm, self).__init__(*args, **kwargs)
        self.product.data = product
        self.user.data = reporter

