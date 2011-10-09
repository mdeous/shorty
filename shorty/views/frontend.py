# -*- coding: utf-8 -*-

from flask import *
from flask.views import MethodView, View

from shorty.core.shortener import shorten_url, expand_url
from shorty.forms import URLForm

frontend = Blueprint('frontend', __name__)


class IndexView(MethodView):
    template = 'index.html'

    def get(self):
        form = URLForm()
        return render_template(self.template,
                               form=form)

    def post(self):
        form = URLForm()
        if not form.validate_on_submit():
            return render_template(self.template,
                                   form=form)
        short_code = shorten_url(form.data['url'])
        short_url = '%s/%s' % (current_app.config['BASE_URL'], short_code)
        return render_template(self.template,
                               form=form,
                               short_url=short_url)


class ShortLinkRedirectView(View):
    methods = ['GET']

    def dispatch_request(self, short_code):
        long_url = expand_url(short_code)
        return redirect(long_url)
