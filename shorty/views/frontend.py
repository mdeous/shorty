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
from sqlalchemy.orm.exc import NoResultFound

from shorty import db
from shorty.models import ShortURL
from shorty.core.shortener import UrlEncoder, EncoderError
from shorty.core.forms import URLForm

frontend = Blueprint('frontend', __name__)


class IndexView(MethodView):
    template = 'index.html'

    def get(self):
        url_form = URLForm()
        return render_template(self.template,
                               url_form=url_form)

    def post(self):
        url_form = URLForm()
        if not url_form.validate_on_submit():
            return render_template(self.template,
                                   url_form=url_form,
                                   current_user=current_user)
        url = url_form.data['url']
        try:
            url_obj = ShortURL.query.filter_by(long_url=url).one()
        except NoResultFound:
            url_obj = ShortURL(long_url=url)
            db.session.add(url_obj)
            db.session.commit()
        short_code = UrlEncoder().encode_id(url_obj.id)
        short_url = '%s/%s' % (current_app.config['BASE_URL'], short_code)
        return render_template(self.template,
                               url_form=url_form,
                               short_url=short_url,
                               current_user=current_user)


class ShortLinkRedirectView(View):
    methods = ['GET']

    def dispatch_request(self, short_code):
        try:
            url_code = short_code.split('/')[-1] if ('/' in short_code) else short_code
            url_id = UrlEncoder().decode_id(url_code)
            url_obj = ShortURL.query.filter_by(id=url_id).one()
            return redirect(url_obj.long_url)
        except EncoderError:
            flash('Unknown short URL', category='error')
            return redirect(url_for('frontend.index'))
