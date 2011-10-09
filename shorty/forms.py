# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, SubmitField
from flask.ext.wtf import Required, Length, URL


class ShortenForm(Form):
    url = TextField('URL', [Required(), Length(max=255), URL()])
    submit = SubmitField('shorten')
