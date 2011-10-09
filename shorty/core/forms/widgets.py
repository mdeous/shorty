# -*- coding: utf-8 -*-

from flask.ext.wtf import TextInput


class XXLargeTextInput(TextInput):
    def __call__(self, field, **kwargs):
        kwargs['class'] = u'xxlarge'
        return super(XXLargeTextInput, self).__call__(field, **kwargs)
