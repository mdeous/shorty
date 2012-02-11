# -*- coding: utf-8 -*-

BASE_URL = 'http://localhost:5000'

PREFIX = '_'

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
