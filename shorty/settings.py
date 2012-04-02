# -*- coding: utf-8 -*-
#    This file is part of Shorty.
#
#    Shorty is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Shorty is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Shorty.  If not, see <http://www.gnu.org/licenses/>.

BASE_URL = 'http://localhost:5000'

DEBUG = False
TESTING = False
ASSETS_DEBUG = DEBUG
DEBUG_TB_ENABLED = DEBUG

SECRET_KEY = 'DuMmY sEcReT kEy'
CSRF_ENABLED = True
CSRF_SESSION_KEY = '_csrf_token'

SQLALCHEMY_DATABASE_URI = 'sqlite:///shorty.sqlite'

LOGGING_LEVEL = 'WARNING'
LOGGING_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGING_FILE_DIR = '.'
LOGGING_FILE_MAX_SIZE = 10*1024*1024

RESOURCES = {
    'css': [
        'css/bootstrap.css',
        'css/shorty.css'
    ],
    'js': [
        'js/jquery-1.7.2.js',
        'js/bootstrap.js',
        'js/shorty.js'
    ]
}

try:
    from .local_settings import *
except ImportError:
    pass
