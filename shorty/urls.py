# -*- coding: utf-8 -*-

from shorty.views.main import main, IndexView

routes = [
    ((main, ''),
        ('/', IndexView.as_view('index')),
    ),
]
