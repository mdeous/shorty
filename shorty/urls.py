# -*- coding: utf-8 -*-

from shorty.views.frontend import frontend, IndexView

routes = [
    ((frontend, ''),
        ('/', IndexView.as_view('index')),
    ),
]
