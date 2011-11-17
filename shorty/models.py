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

from datetime import datetime

from flask.ext.login import UserMixin, make_secure_token
from sqlalchemy.ext.declarative import declared_attr
#from werkzeug.utils import cached_property

from shorty import db


class AutoInitModelMixin(object):
    """
    Mixin for populating models' columns automatically (no need to
    define an __init__ method) and set the default value if any.
    Also sets the model's id and __tablename__ automatically.
    """
    id = db.Column(db.Integer, primary_key=True)

    # use the lowercased class name as the __tablename__
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __init__(self, *args, **kwargs):
        for attr in (a for a in dir(self) if not a.startswith('_')):
            attr_obj = getattr(self, attr)
            if isinstance(attr_obj, db.Column):
                if attr in kwargs:
                    setattr(self, attr, kwargs[attr])
                else:
                    if hasattr(attr_obj, 'default'):
                        if callable(attr_obj.default):
                            setattr(self, attr, attr_obj.default())
                        else:
                            setattr(self, attr, attr_obj.default)


class ShortURL(db.Model, AutoInitModelMixin):
    long_url = db.Column(db.String(255), unique=True)
    created = db.Column(db.DateTime, default=datetime.now)
#    clicks = db.relationship("Click")

    def __repr__(self):
        return "<ShortURL: '%s'>" % self.long_url


class User(db.Model, AutoInitModelMixin, UserMixin):
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(54))
    active = db.Column(db.Boolean, default=False)
    authenticated = False

    @classmethod
    def from_token(cls, token):
        for user in User.query.all():
            if make_secure_token(user.name, user.password) == token:
                return user
        return None

    def get_auth_token(self):
        return make_secure_token(self.name, self.password)

    def is_active(self):
        return self.active


#class Click(db.Model, AutoInitModelMixin):
#    url_id = db.Column(db.Integer, db.ForeignKey('shorturl.id'))
#    user_agent = db.Column(db.String(255), default='Unknown')
#    time = db.Column(db.DateTime, default=datetime.now)
#    #TODO: locate originating country/city
#    #TODO: parse the user-agent to extract OS/browser_name/browser_version
#
#    @cached_property
#    def url(self):
#        return ShortURL.query.filter_by(id=self.url_id).one()
#
#    def __repr__(self):
#        return "<Click on '%s'>" % self.url.long_url
