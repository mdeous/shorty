# -*- coding: utf-8 -*-
#    This file is part of Shorty.
#
#    Shorty is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Shorty is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shorty.  If not, see <http://www.gnu.org/licenses/>.

from flask import *
from flask.ext.login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from shorty import db
from shorty.models import User
from shorty.core.forms import RegisterForm, LoginForm
from shorty.core.log import getLogger

users = Blueprint('users', __name__)
logger = getLogger(__name__)

PASSWORD_REQUIREMENTS_STR = """
<ul>
<li>At least 12 characters long</li>
<li>Contains at least 1 uppercase letter</li>
<li>Contains at least 1 lowercase letter</li>
<li>Contains at least 1 digit</li>
</ul>
"""


@users.route('/login', methods=('GET', 'POST'))
def login():
    tpl = 'users/login.html'
    form = LoginForm()

    if request.method == 'POST':
        login_success = True
        if not form.validate_on_submit():
            return render_template(tpl,
                login_form=form
            )
        username = form.data['username']
        try:
            user = User.query.filter_by(name=username).one()
        except NoResultFound:
            logger.warning("login attempt with unknown username '%s'" % username)
            flash("Invalid username or password", category='error')
            login_success = False
        else:
            if not check_password_hash(user.password, form.data['password']):
                logger.warning("login failed for username '%s'" % username)
                flash("Invalid username or password", category='error')
                login_success = False
            else:
                login_user(user)
                logger.info("successful login for '%s'" % username)
                flash("Log in successful", category='success')
        if login_success:
            return redirect(url_for('frontend.index'))
        return render_template(tpl,
            login_form=form
        )

    return render_template(tpl,
        login_form=form,
    )

@users.route('/register', methods=('GET', 'POST'))
def register():
    tpl = 'users/register.html'
    form = RegisterForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template(tpl,
                reg_form=form
            )
        username = form.data['username']
        user_obj = User(
            name=username,
            email=form.data['email'],
            password=generate_password_hash(form.data['password']),
            active=True
        )
        db.session.add(user_obj)
        try:
            db.session.commit()
        except IntegrityError:
            logger.info("failed registration attempt for '%s'" % username)
            flash('An user already exists with given details', category='error')
        else:
            logger.info("user '%s' successfully registered" % username)
            flash('Registration complete. You can sign in.', category='info')
        return redirect(url_for('frontend.index'))

    return render_template(tpl,
        reg_form=form,
        password_requirements=PASSWORD_REQUIREMENTS_STR
    )

@users.route('/logout', methods=('POST',))
def logout():
    if current_user.is_authenticated():
        logout_user()
        logger.info("user '%s' logged out" % current_user.username)
        flash("Successfully logged out", category='success')
    else:
        logger.info("logout attempt from unauthenticated user")
        flash("You're not authenticated", category='error')
    return ''

@users.route('/profile')
def profile():
    return render_template('users/profile.html',
        current_user=current_user
    )

@users.route('/links')
def links():
    links = current_user.shorturls.all()
    return render_template('users/links.html',
        links=links
    )
