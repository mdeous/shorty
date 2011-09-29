# -*- coding: utf-8 -*-

def static_files():
    STATIC_ROOT = '/static'
    return dict(
        STATIC_ROOT = STATIC_ROOT,
        CSS_PATH = '%s/css' % STATIC_ROOT,
        JS_PATH = '%s/js' % STATIC_ROOT,
    )
