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
from flask.views import MethodView, View
from flask.ext.login import current_user, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from shorty import db
from shorty.models import User
from shorty.core.forms import RegisterForm, LoginForm

users = Blueprint('users', __name__)


class LoginView(View):
    methods = ['POST']

    def dispatch_request(self):
        form = LoginForm()
        if not form.validate_on_submit():
            #TODO: find a nice way to display errors for this form
            flash("An error occured while logging in", category='error')
            return redirect(url_for('frontend.index'))
        try:
            user = User.query.filter_by(name=form.data['username']).one()
        except NoResultFound:
            flash("Invalid username or password", category='error')
        else:
            if not check_password_hash(user.password, form.data['password']):
                flash("Invalid username or password", category='error')
            else:
                login_user(user)
                flash("Log in successful", category='success')
        return redirect(url_for('frontend.index'))


class RegisterView(MethodView):
    template = 'register.html'

    def get(self):
        reg_form = RegisterForm()
        return render_template(self.template, reg_form=reg_form)

    def post(self):
        reg_form = RegisterForm()
        if not reg_form.validate_on_submit():
            return render_template(self.template, reg_form=reg_form)
        user_obj = User(
            name=reg_form.data['username'],
            email=reg_form.data['email'],
            password=generate_password_hash(reg_form.data['password']),
            active=True
        )
        db.session.add(user_obj)
        try:
            db.session.commit()
        except IntegrityError:
            #TODO: notify user about what fields are duplicate (or not?)
            flash('An user already exists with given details', category='error')
        else:
            flash('Registration complete. You can sign in.', category='info')
        return redirect(url_for('frontend.index'))


class LogoutView(MethodView):
    def post(self):
        if current_user.is_authenticated():
            logout_user()
            flash("Successfuly logged out", category='success')
        else:
            flash("You're not authenticated", category='error')
        return redirect(url_for('frontend.index'))
