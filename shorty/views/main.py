# -*- coding: utf-8 -*-

from flask import *
from flask.views import MethodView

main = Blueprint('main', __name__)


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')
