import flask
from flask.ext import wtf
from wtforms import (
        TextField, SelectField, validators, PasswordField,
        TextAreaField, FileField, StringField, DateTimeField)
import datetime
import requests

class LoginForm(wtf.Form):
    """ Form to log in the application. """
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

def get_component_choices(product_id):
    components = requests.get('http://127.0.0.1:9998/components/'+str(product_id)).json()
    component_choices = []
    for key in components:
        component = components[key][1:]
        component_choices.append(tuple(component[::-1]))
    return component_choices

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

def get_product(product_id):
    return 'Fedora'

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
            'Component', [validators.Required()], description=(
                "Components are second-level categories; each belongs to a "
                "particular Product. Select a Product to narrow down "
                "this list."))
    version = SelectField(
        'Version', [validators.Required()], choices=get_fedora_versions())
    severity = SelectField('Severity', choices=get_severity())
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
    reported = DateTimeField('Reported')

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', '')
        reporter = kwargs.pop('reporter', '')
        initial_data = kwargs.pop('initial_data', {})
        readonly = kwargs.pop('readonly', False)
        super(BugForm, self).__init__(*args, **kwargs)
        self.product.data = get_product(product_id)
        self.user.data = reporter
        for key, value in initial_data.items():
            if key == "reporter_email":
                field = getattr(self, "user", None)
            else:
                field = getattr(self, key, None)
            if field:
                if key == 'reported':
                    field.data = datetime.datetime.strptime(value[:19], '%Y-%m-%d %H:%M:%S')
                else:
                    field.data = value
        if not readonly:
            self.component_id.choices = get_component_choices(product_id)
