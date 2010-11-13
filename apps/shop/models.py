# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Shop Application Models

"""
from google.appengine.ext import db
from tipfy.ext.db import SlugProperty

from apps.tagging.models import Taggable


class Product(Taggable):
    name = db.StringProperty(required=True)
    slug = SlugProperty(name)
    description = db.TextProperty(required=True)
    live = db.BooleanProperty(required=True)
    price = db.FloatProperty(required=True)
    unit = db.StringProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    modified = db.DateTimeProperty(required=True, auto_now=True)
    
    @classmethod
    def get_products_by_tag(self, tag):
        query = self.all()
        query.filter('live =', True)
        query.filter('tags IN', [tag])
        query.order('-modified')
        return query.fetch(10)
    
    @classmethod
    def get_product_by_slug(self, slug=None):
        query = self.all().filter('slug =', slug).filter('live =', True)
        return query.get()
    
    @classmethod
    def get_latest_products(self, count=10):
        query = self.all().filter('live =', True).order('-modified')
        return query.fetch(count)


class Order(db.Model):
    """
    should hold:
        - a list of items
        - user reference
        - datetime posted
        - comment
    """

