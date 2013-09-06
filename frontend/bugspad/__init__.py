from __future__ import absolute_import
import os

import flask
import vobject
from functools import wraps
#from sqlalchemy.exc import SQLAlchemyError

from .bsession import RedisSessionInterface
from .forms import BugForm

# import forms as forms


# Create the application.
APP = flask.Flask(__name__)
# set up FAS
# APP.config.from_object('bugspad.default_config')
APP.session_interface = RedisSessionInterface()
APP.secret_key = 'A0Zr98j/3yXRT'


@APP.route('/')
def index():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('index.html')

@APP.route('/login/', methods=('GET', 'POST'))
def auth_login():
    """ Method to log into the application using FAS OpenID. """
    from flask_fas_openid import FAS
    FAS = FAS(APP)
    return_point = flask.url_for('index')
    if 'next' in flask.request.args:
        return_point = flask.request.args['next'] 
    
    if flask.g.fas_user:
        return flask.redirect(return_point)

    return FAS.login(return_url=return_point)


@APP.route('/logout/')
def auth_logout():
    """ Method to log out from the application. """
    from flask_fas_openid import FAS
    FAS = FAS(APP)
    if not flask.g.fas_user:
        return flask.redirect(flask.url_for('index'))
    FAS.logout()
    flask.flash('You have been logged out')
    return flask.redirect(flask.url_for('index'))


@APP.route('/bugs/new/', methods=('GET', 'POST'))
def bug_create():
    form = BugForm()
    if form.validate_on_submit():
        pass
        # handler = BugspadHandler()
        # bug_id = handler.create_bug(form.data)
        # return flask.redirect('/bug/' + bug_id + '/')
    return flask.render_template('bug.html', form=form)

@APP.route('/bugs/new/products/')
def select_product():
    import bugspad.products as products
    data = products.get_products()
    return flask.render_template('products.html', products=data)