# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr
from werkzeug.utils import cached_property

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
    slug = db.Column(db.String(30), unique=True)
    created = db.Column(db.DateTime, default=datetime.now)
    clicks = db.relationship("Click")

    def __repr__(self):
        return "<ShortURL: '%s'>" % self.long_url


class Click(db.Model, AutoInitModelMixin):
    url_id = db.Column(db.Integer, db.ForeignKey('shorturl.id'))
    user_agent = db.Column(db.String(255), default='Unknown')
    time = db.Column(db.DateTime, default=datetime.now)
    #TODO: locate originating country/city
    #TODO: parse the user-agent to extract OS/browser_name/browser_version

    @cached_property
    def url(self):
        return ShortURL.query.filter_by(id=self.url_id).one()

    def __repr__(self):
        return "<Click on '%s'>" % self.url.long_url
