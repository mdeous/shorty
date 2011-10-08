# -*- coding: utf-8 -*-

def static_files():
    STATIC_ROOT = '/static'
    return dict(
        STATIC_ROOT = STATIC_ROOT,
        CSS = '%s/css' % STATIC,
        JS = '%s/js' % STATIC,
    )
