# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, SubmitField
from flask.ext.wtf import Required, Length, URL

from shorty.core.forms.widgets import XXLargeTextInput


class URLForm(Form):
    url = TextField('URL', [Required(), Length(max=255), URL()], widget=XXLargeTextInput())
    submit = SubmitField('shorten')
