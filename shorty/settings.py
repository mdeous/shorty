# -*- coding: utf-8 -*-

APP_DEBUG = True
APP_SECRET_KEY = 'DuMmY sEcReT kEy'

DATABASE_URI = 'sqlite:///shorty.sqlite'

try:
    from .local_settings import *
except ImportError:
    pass
