# -*- coding: utf-8 -*-

from flask import *
from flask.views import MethodView, View

from shorty.core.shortener import shorten_url, expand_url, expand_slug, EncoderError
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
        short_code = shorten_url(form.data['url'], form.data.get('slug', ''))
        short_url = '%s/%s%s' % (current_app.config['BASE_URL'], current_app.config['PREFIX'], short_code)
        return render_template(self.template,
                               form=form,
                               short_url=short_url)


class ShortLinkRedirectView(View):
    methods = ['GET']

    def dispatch_request(self, short_code):
        if short_code.startswith(current_app.config['PREFIX']):
            try:
                long_url = expand_url(short_code[len(current_app.config['PREFIX']):])
                return redirect(long_url)
            except EncoderError:
                flash('Unknown short URL', category='error')
                return redirect(url_for('frontend.index'))
        else:
            long_url = expand_slug(short_code)
            return redirect(long_url)
