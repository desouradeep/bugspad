from __future__ import absolute_import
import os

import flask
import vobject
from functools import wraps
#from sqlalchemy.exc import SQLAlchemyError
from flask_fas_openid import FAS

from .bsession import RedisSessionInterface
from .forms import BugForm
from .utils import BugspadBackendAPI

# import forms as forms


# Create the application.
APP = flask.Flask(__name__)
# set up FAS
# APP.config.from_object('bugspad.default_config')
APP.session_interface = RedisSessionInterface()
APP.secret_key = 'A0Zr98j/3yXRT'
FAS = FAS(APP)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.g.fas_user is None:
            return flask.redirect(flask.url_for('auth_login', next=flask.request.url))
        return f(*args, **kwargs)
    return decorated_function


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

@APP.route('/login/', methods=('GET', 'POST'))
def auth_login():
    """ Method to log into the application using FAS OpenID. """
    return_point = flask.url_for('index')
    if 'next' in flask.request.args:
        return_point = flask.request.args['next']
    if flask.g.fas_user:
        return flask.redirect(return_point)

    return FAS.login(return_url=return_point)


@APP.route('/logout/')
def auth_logout():
    """ Method to log out from the application. """
    if not flask.g.fas_user:
        return flask.redirect(flask.url_for('index'))
    FAS.logout()
    flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('index'))


@APP.route('/bugs/new/products/<product_id>', methods=('GET', 'POST'))
@login_required
def bug_create(product_id):
    form = BugForm(product_id=product_id, reporter=flask.g.fas_user.email)
    if form.validate_on_submit():
        backend_obj = BugspadBackendAPI()
        bug_id = backend_obj.create_bug(form.data)
        return flask.redirect('/bug/%d/' % bug_id)
    return flask.render_template('bug_create.html', form=form, product=product_id)

@APP.route('/bug/<int:bug_id>/', methods=('GET',))
def bug_details(bug_id):
    api_obj = BugspadBackendAPI()
    bug_details = api_obj.bug_details(bug_id)
    form = BugForm(initial_data=bug_details, readonly=True)
    return flask.render_template('bug_view.html', form=form, bug_details=bug_details)


@APP.route('/bug/<int:bug_id>/edit', methods=('GET', 'POST'))
@login_required
def bug_edit(bug_id):
    api_obj = BugspadBackendAPI()
    bug_details = api_obj.bug_details(bug_id)
    form = BugForm(initial_data=bug_details, product_id=1)
    if form.validate_on_submit():
        api_obj.update_bug(form.data)
        return flask.redirect('/bug/%d' % bug_id)
    return flask.render_template('bug_edit.html', form=form, bug_details=bug_details)


@APP.route('/bugs/new/products/')
def select_product():
    import bugspad.products as products
    data = products.get_products()
    return flask.render_template('products.html', products=data)
