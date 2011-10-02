# -*- coding: utf-8 -*-

DEBUG = True
TESTING = False

SECRET_KEY = 'DuMmY sEcReT kEy'
SESSION_COOKIE_SECURE = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///shorty.sqlite'

try:
    from .local_settings import *
except ImportError:
    pass
