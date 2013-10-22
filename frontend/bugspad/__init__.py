from __future__ import absolute_import
import os

import flask
import vobject
from functools import wraps
#from sqlalchemy.exc import SQLAlchemyError
from flask_fas_openid import FAS

from .bsession import RedisSessionInterface
from .forms import BugForm
from .utils import BugspadBackendAPI, Paginate
import requests
# import forms as forms
from datetime import datetime
from time import strftime

from flask import Blueprint
from flask.ext.paginate import Pagination
mod = Blueprint('all_bugs', __name__)

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

@APP.route('/bugs/<int:bug_id>/', methods=('GET',))
def bug_details(bug_id):
    api_obj = BugspadBackendAPI()
    bug_details = api_obj.bug_details(bug_id)
    form = BugForm(initial_data=bug_details, readonly=True)
    return flask.render_template('bug_view.html', form=form, bug_details=bug_details)


@APP.route('/bugs/<int:bug_id>/edit', methods=('GET', 'POST'))
@login_required
def bug_edit(bug_id):
    if flask.request.method == 'POST' and flask.request.is_xhr == True:
        comment_text = flask.request.values['comment']
        json_data = {'user': flask.g.fas_user.fullname,
                     'password' : '',
                     'bug_id' : bug_id,
                     'desc' : comment_text
        }
        requests.post('http://127.0.0.1:9998/comment', json_data)
        post_time = datetime.now().strftime('%Y-%m-%d %X')
        no = flask.request.values['comment_number']
        comment_html = '''
        <br>
        <div class="panel-group col-xs-12 new-comment" id="comments-accordion">
            <div class='panel panel-info'>
                <div class="panel-heading">
                    <div class='panel-title'>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#comments-accordion" href="#comment%s">
                            Description by <strong>%s</strong> <span class="pull-right">%s</span>
                        </a>
                    </div>
                </div>
                <div id="comment%s" class="panel-body collapse in">
                <div class="accordion-inner">
                            %s
                    </div>
                </div>
            </div>
        </div>
        ''' % (no, flask.g.fas_user.fullname, post_time, no, comment_text)
        return flask.make_response(flask.jsonify({'post':True ,'comment_html': comment_html }), 200)

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

@APP.route('/bugs/products/<int:product_id>')
def bugs_list(product_id):
    backend_obj = BugspadBackendAPI()
    all_bugs = backend_obj.get_bugs(product_id)

    if flask.request.method == 'GET' and flask.request.is_xhr == True:
        page = int(flask.request.values['page'])
        per_page = int(flask.request.values['per_page'])
        paging_obj = Paginate(per_page=per_page,
                              page=page,
                              total_records=len(all_bugs)
                        )
        paging_start, paging_end = paging_obj.get_numbers()
        show_bugs = all_bugs[(paging_obj.page-1)*paging_obj.per_page:(paging_obj.page)*paging_obj.per_page]
        row_html = ''
        for bug in show_bugs:
            row_html += '<tr class=\'table-row\'>'
            for data in bug:
                row_html += '<td>'+str(data)+'</td>'
            row_html += '</tr>'

        paging_html = '<li class="paging"><a href="/bugs/products/1">First</a></li>'
        for page in range(paging_start,paging_end+1):
            paging_html += '''
            <li id='page-%s' class="paging"><a href='javascript: void(0)'>%s</a></li>
            ''' % (page, page)
        paging_html += '<li id="page-%s" class="paging"><a href="javascript: void(0)"> Last</a></li>' % (paging_obj.paging_max_end)

        return flask.make_response(
            flask.jsonify({'get':True , 'row_html': row_html,
                'paging_html' : paging_html,
                'page_total' : paging_obj.paging_max_end,
                'current_page' : page,
                }), 200)

    page = int(flask.request.args.get('page', 1))
    paging_obj = Paginate(per_page=20, page=page, total_records=len(all_bugs))
    paging_start, paging_end = paging_obj.get_numbers()
    return flask.render_template('bug_list.html',
        all_bugs= all_bugs[(paging_obj.page-1)*paging_obj.per_page:(paging_obj.page)*paging_obj.per_page],
        paging=range(paging_start,paging_end+1),
        page_total = paging_obj.paging_max_end,
        current_page = page-1,
    )