# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Daily Offer Models

"""
import logging

from google.appengine.ext import db
from tipfy.ext.db import SlugProperty

from apps.files.models import File


class Offer(db.Model):
    title = db.StringProperty(required=True)
    slug = SlugProperty(title)
    intro = db.TextProperty(required=True)
    content = db.TextProperty()
    live = db.BooleanProperty(required=True)
    promoted = db.BooleanProperty(required=True)
    language = db.StringProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    modified = db.DateTimeProperty(required=True, auto_now=True)
    photo = db.ReferenceProperty(File)
    
    @classmethod
    def get_by_slug(self, slug=None, language=None):
        query = self.all().filter('slug =', slug).filter('live =', True)
        query.filter('language =', language)
        return query.get()
    
    @classmethod
    def get_latest_offer(self, slug=None, language=None):
        query = self.all().order('-modified').filter('live =', True).filter('language =', language)
        return query.get()