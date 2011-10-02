#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager

from shorty import app

manager = Manager(app)


class SyncDB(Command):
    """
    Initializes the database tables.
    """
    def run(self):
        from shorty import db
        db.drop_all()
        db.create_all()
        db.session.commit()


manager.add_command('syncdb', SyncDB())
manager.run()
