# -*- coding: utf-8 -*-

def static_files():
    STATIC_ROOT = '/static'
    return dict(
        STATIC_ROOT = STATIC_ROOT,
        CSS = '%s/css' % STATIC_ROOT,
        JS = '%s/js' % STATIC_ROOT,
    )
