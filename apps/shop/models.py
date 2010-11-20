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
    def get_latest_products(self, count=10, live=True):
        query = self.all()
        if live:
            query.filter('live =', live)
        query.order('-modified')
        return query.fetch(count)


class Order(db.Model):
    """
    should hold:
        - a list of items + amount ( [ [5,10], [10,10] ] )
        - user reference
        - datetime posted
        - comment
        - delivered (default False)
        - delivery info
    eg. 5 pack of Black Coffee and 2 pack of Green Tea ordered by Anna at 2010.10.11. 20:00 and she wants it to be delivered at 2010.10.15. 1102-Budapest Körösi Csoma Sándor út 43.
    
    """
    items = db.ListProperty(item_type=str, required=True)
    user = db.IntegerProperty(required=True, default=1)
    comment = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    delivered = db.BooleanProperty(default=False)
    delivery_info = db.TextProperty(required=True)


