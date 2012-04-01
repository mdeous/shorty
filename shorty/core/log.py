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

import os
import sys
from logging import *
from logging.handlers import RotatingFileHandler

from shorty import settings


class ColorFormatter(Formatter):
    """
    A logging formatter that displays the loglevel with colors and
    the logger name in bold.
    """
    _colors_map = {
        'DEBUG': '\033[22;32m',
        'INFO': '\033[01;34m',
        'WARNING': '\033[22;35m',
        'ERROR': '\033[22;31m',
        'CRITICAL': '\033[01;31m'
    }

    def format(self, record):
        """
        Overrides the default :func:`logging.Formatter.format` to add colors to
        the :obj:`record`'s :attr:`levelname` and :attr:`name` attributes.
        """
        level_length = len(record.levelname)
        if record.levelname in self._colors_map:
            record.msg = '{0}{1}\033[0;0m'.format(
                self._colors_map[record.levelname],
                record.msg
            )
            record.levelname = '{0}{1}\033[0;0m'.format(
                self._colors_map[record.levelname],
                record.levelname
            )
        record.levelname += ' ' * (8 - level_length)
        record.name = '\033[37m\033[1m{0}\033[0;0m'.format(record.name)
        return super(ColorFormatter, self).format(record)


# prepare formatters
console_formatter = ColorFormatter(
    settings.LOGGING_FORMAT,
    settings.LOGGING_DATE_FORMAT
)

# prepare handlers
_handlers = []

console_handler = StreamHandler(stream=sys.stdout)
console_handler.setFormatter(console_formatter)
console_handler.setLevel(settings.LOGGING_LEVEL)
_handlers.append(console_handler)

# configure logging
logger = getLogger()
logger.setLevel(settings.LOGGING_LEVEL)
for h in _handlers:
    logger.addHandler(h)
