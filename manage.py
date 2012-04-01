#!/usr/bin/env python
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

from flask.ext.assets import ManageAssets
from flask.ext.script import Command, Manager, Shell, Server, Option

from shorty import app, assets

manager = Manager(app)


class SyncDB(Command):
    """
    Initializes the database tables.
    """
    def run(self):
        from shorty import db
        from shorty.models import User
        app.config['SQLALCHEMY_ECHO'] = True
        db.drop_all()
        db.create_all()
        anonymous_user = User(
            name='AnonymousUser',
            email='anonymous.user@example.com',
            password=54*'0',
            active=False
        )
        db.session.add(anonymous_user)
        db.session.commit()


class FixedShell(Shell):
    """
    Runs a Python shell inside Flask application context.
    """
    def run(self, no_ipython):
        context = self.get_context()
        if not no_ipython:
            try:
                from IPython.frontend.terminal.embed import InteractiveShellEmbed
                sh = InteractiveShellEmbed(banner1=self.banner)
                sh(global_ns=dict(), local_ns=context)
                return
            except ImportError:
                pass
        from code import interact
        interact(banner=self.banner, local=context)


class Test(Command):
    """
    Runs the application's unit tests.
    """
    def run(self):
        import os
        from unittest import TestLoader, TextTestRunner
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        loader = TestLoader()
        test_suite = loader.discover(cur_dir)
        runner = TextTestRunner(verbosity=2)
        runner.run(test_suite)


class RunCommand(Command):
    """
    Base class for commands used to run the application (ie. takes options
    to specify the host/port).
    """
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port

    def get_options(self):
        options = (
            Option('-t', '--host',
                   dest='host',
                   default=self.host),
            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),
        )
        return options

    def run(self, host, port):
        raise NotImplementedError


class RunServer(Server):
    def handle(self, app, *args, **kwargs):
        app.config['SQLALCHEMY_ECHO'] = True
        super(RunServer, self).handle(app, *args, **kwargs)


class RunTornado(RunCommand):
    """
    Serves the application using Tornado.
    """
    def run(self, host, port):
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(port=port, address=host)
        IOLoop.instance().start()


del manager._commands['shell']
del manager._commands['runserver']
manager.add_command('shell', FixedShell())
manager.add_command('syncdb', SyncDB())
manager.add_command('test', Test())
manager.add_command('runserver', RunServer())
manager.add_command('tornado', RunTornado())
manager.add_command('assets', ManageAssets(assets))
manager.run()
