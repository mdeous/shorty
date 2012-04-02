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
from flask.views import MethodView
from shorty.core.shortener import UrlEncoder, EncoderError
from shorty.models import ShortURL

api = Blueprint('api', __name__)


class ResolveView(MethodView):
    def get(self, short_code):
        try:
            url_code = short_code.split('/')[-1] if ('/' in short_code) else short_code
            url_id = UrlEncoder().decode_id(url_code)
            url_obj = ShortURL.query.get(url_id)
            ret = { 'success': { "url": url_obj.long_url } }
        except EncoderError:
            ret = { 'errors':  ['Unknow short URL'] }
        return jsonify(ret)
api.add_url_rule('/resolve/<short_code>', view_func=ResolveView.as_view('resolve'))
