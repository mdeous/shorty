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

from flask.ext.sqlalchemy import SQLAlchemy

from shorty import settings
from shorty.core import create_app, create_login_manager, setup_routing, create_assets_manager
from shorty.core.log import getLogger

logger = getLogger(__name__)

# setup application
logger.info("creating WSGI application")
app = create_app(settings)

# setup database
logger.info("setting up SQLAlchemy")
db = SQLAlchemy(app)

# setup routes and blueprints
logger.info("registering routes")
from shorty.urls import routes
setup_routing(app, routes)

# setup the login manager
logger.info("setting up login management")
login_manager = create_login_manager(app)

# setup static files
logger.info("preparing static files")
assets = create_assets_manager(app)
