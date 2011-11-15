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

from shorty.core.forms import RegisterForm

users = Blueprint('users', __name__)


class LoginView(View):
    methods = ['POST']

    def dispatch_request(self):
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
        return redirect(url_for('users.register'))
