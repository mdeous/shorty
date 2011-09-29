# -*- coding: utf-8 -*-

from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy

from shorty import settings
from shorty.context_processors import static_files
from shorty.core import setup_routing

# setup application
app = Flask('shorty')
app.debug = settings.APP_DEBUG
app.secret_key = settings.APP_SECRET_KEY

# setup database
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
db = SQLAlchemy(app)

# register application views and blueprints
from shorty.urls import routes
setup_routing(app, routes)

# register context processors
app.context_processor(static_files)
