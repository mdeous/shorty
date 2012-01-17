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
from flask.ext.login import current_user

from shorty.core.shortener import shorten_url, expand_url, EncoderError
from shorty.core.forms import URLForm, LoginForm

frontend = Blueprint('frontend', __name__)


class IndexView(MethodView):
    template = 'index.html'

    def get(self):
        url_form = URLForm()
        login_form = LoginForm()
        return render_template(self.template,
                               url_form=url_form,
                               login_form=login_form)

    def post(self):
        form = URLForm()
        if not form.validate_on_submit():
            return render_template(self.template,
                                   form=form,
                                   current_user=current_user)
        short_code = shorten_url(form.data['url'])
        short_url = '%s/%s' % (current_app.config['BASE_URL'], short_code)
        return render_template(self.template,
                               form=form,
                               short_url=short_url,
                               current_user=current_user)


class ShortLinkRedirectView(View):
    methods = ['GET']

    def dispatch_request(self, short_code):
        try:
            long_url = expand_url(short_code)
            return redirect(long_url)
        except EncoderError:
            flash('Unknown short URL', category='error')
            return redirect(url_for('frontend.index'))
