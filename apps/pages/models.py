# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Page Models

"""
import logging

from google.appengine.ext import db
from tipfy.ext.db import SlugProperty


class Page(db.Model):
    title = db.StringProperty(required=True)
    slug = SlugProperty(title)
    content = db.TextProperty(required=True)
    live = db.BooleanProperty(required=True)
    language = db.StringProperty(required=True)
    
    @classmethod
    def get_page_by_slug(self, slug=None, language=None):
        query = self.all().filter('slug =', slug).filter('live =', True)
        query.filter('language =', language)
        return query.get()