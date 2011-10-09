# -*- coding: utf-8 -*-

from shorty.views.frontend import frontend, IndexView, ShortLinkRedirectView

routes = [
    ((frontend, ''),
        ('/', IndexView.as_view('index')),
        ('/<short_code>', ShortLinkRedirectView.as_view('redir')),
    ),
]
