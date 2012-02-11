# -*- coding: utf-8 -*-

import re
from flask.ext.wtf import Form, TextField, TextInput, SubmitField
from flask.ext.wtf import Required, Optional, Length, URL, Regexp

from shorty.core.forms.widgets import XXLargeTextInput

RE_SLUG = re.compile(r'^[-\w]+$')

class URLForm(Form):
    url = TextField('URL', [Required(), Length(max=255), URL()], widget=XXLargeTextInput())
    slug = TextField('Slug', [Optional(), Length(max=30), Regexp(RE_SLUG)], widget=TextInput())
    submit = SubmitField('shorten')
