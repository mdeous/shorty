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

from flask import flash, redirect, url_for, request

from shorty import settings
from shorty.core.log import getLogger

logger = getLogger(__name__)


def _unauthorized_callback():
    logger.warning("%s: unauthorized access attempt" % request.endpoint)
    flash("You must be logged in to view this page.", category='error')
    return redirect(url_for('frontend.index'))

def setup_routing(app, routes):
    """
    Registers :class:`flask.Blueprint` instances and adds routes all at once.

    :param app: The current application.
    :type app: flask.Flask.
    :param routes: The routes definition in the format:
        ((blueprint_instance, url_prefix),
            ('/route1/<param>', view_function1),
            ('/route2', view_function2),
            ...
        )
    :type routes: list.
    :returns: None
    """
    for route in routes:
        # endpoint: (blueprint_instance, url_prefix)
        # rules: [('/route/', view_function), ...]
        endpoint, rules = route[0], route[1:]
        for pattern, view in rules:
            if endpoint is None:
                app.add_url_rule(pattern, view_func=view)
            else:
                endpoint[0].add_url_rule(pattern, view_func=view)
            logger.debug("setup_routing(): adding '%s' view for %s" % (
                view.func_name, pattern
            ))
        if endpoint is not None:
            bp, prefix = endpoint
            msg_suffix = (' on %s' % prefix) if prefix else ' on /'
            logger.debug("setup_routing(): mounting '%s' blueprint%s" % (
                bp.name, msg_suffix
            ))
            app.register_blueprint(bp, url_prefix=prefix)

def create_app(settings_obj, **other_settings):
    from flask import Flask
    from shorty.template_filters import make_short_link

    app = Flask('shorty')
    app.config.from_object(settings_obj)
    for key, val in other_settings.iteritems():
        app.config[key] = val
    app.jinja_env.filters['make_short_link'] = make_short_link
    if app.debug and app.config['ENABLE_DEBUGTOOLBAR']:
        from flask.ext.debugtoolbar import DebugToolbarExtension
        dt = DebugToolbarExtension(app)
    return app

def create_login_manager(app):
    from flask.ext.login import LoginManager
    from shorty.models import User

    login_manager = LoginManager()
    login_manager.setup_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_message = "You need to login"
    login_manager.needs_refresh_message = "You need to re-authenticate"
    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.login'
    login_manager.unauthorized_callback = _unauthorized_callback
    login_manager.user_loader(lambda userid: User.query.get(int(userid)))
    login_manager.token_loader(lambda token: User.from_token(token))
    return login_manager

def create_assets_manager(app):
    from flask.ext.assets import Bundle, Environment

    logger.debug("create_assets_manager(): generating bundle for CSS files")
    assets_env = Environment(app)
    css = Bundle(
        *settings.RESOURCES['css'],
        filters='yui_css',
        output='css/packed.css'
    )
    assets_env.register('css', css)

    logger.debug("create_assets_manager(): generating bundle for JavaScript files")
    js = Bundle(
        *settings.RESOURCES['js'],
        filters='yui_js',
        output='css/packed.js'
    )
    assets_env.register('js', js)

    return assets_env
