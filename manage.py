#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskext.script import Command, Manager

from shorty import app, db

manager = Manager(app)


class RunServer(Command):
    """
    Starts the application using Flask's integrated server.
    """
    def run(self):
        app.run(port=8000)


class SetupDB(Command):
    """Initialize the database tables."""
    def run(self):
        db.create_all()
        db.session.commit()


del manager._commands['runserver']
manager.add_command('runserver', RunServer())
manager.add_command('setupdb', SetupDB())
manager.run()
