#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Command, Manager, Shell

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


del manager._commands['shell']
manager.add_command('shell', FixedShell())
manager.add_command('syncdb', SyncDB())
manager.add_command('test', Test())
manager.run()
