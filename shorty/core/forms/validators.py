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

from flask.ext.wtf import ValidationError

import re


class StrongPassword(object):
    _re_lower = re.compile(r'[a-z]')
    _re_upper = re.compile(r'[A-Z]')
    _re_digit = re.compile(r'\d')
    _re_special = re.compile(r'[^a-zA-Z0-9]')

    def __init__(self,
                 min_length=8,
                 lowercase=True,
                 uppercase=True,
                 digit=True,
                 special=True):
        self.min_length = min_length
        self.lowercase = lowercase
        self.uppercase = uppercase
        self.digit = digit
        self.special = special

    def __call__(self, form, field):
        if len(field.data) < self.min_length:
            raise ValidationError('Must be at least %d characters long' % self.min_length)
        if self.lowercase and self._re_lower.search(field.data) is None:
            raise ValidationError('Must contain at least 1 lowercase character')
        if self.uppercase and self._re_upper.search(field.data) is None:
            raise ValidationError('Must contain at least 1 uppercase character')
        if self.digit and self._re_digit.search(field.data) is None:
            raise ValidationError('Must contain at least 1 digit')
        if self.special and self._re_special.search(field.data) is None:
            raise ValidationError('Must contain at least 1 special character')
