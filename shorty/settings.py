# -*- coding: utf-8 -*-

SHORTY_HOSTNAME = 'localhost'

DEBUG = True
TESTING = False

SECRET_KEY = 'DuMmY sEcReT kEy'
CSRF_ENABLED = True
CSRF_SESSION_KEY = '_csrf_token'

SQLALCHEMY_DATABASE_URI = 'sqlite:///shorty.sqlite'

try:
    from .local_settings import *
except ImportError:
    pass
