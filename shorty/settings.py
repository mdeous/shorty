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

BASE_URL = 'http://localhost'

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
