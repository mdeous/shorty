#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskext.script import Command, Manager

from shorty import app

manager = Manager(app)


class RunServer(Command):
    """
    Starts the application using Flask's integrated server.
    """
    def run(self):
        app.run(port=8000)


del manager._commands['runserver']
manager.add_command('runserver', RunServer())
manager.run()
