# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Shop Application Models

"""
import logging

from google.appengine.ext import db
from tipfy.ext.db import SlugProperty
from tipfy.ext.auth.model import User

from apps.tagging.models import Taggable
from helpers import calculate_total_price, make_list_from_string, extract_ids_from_product_list


class Product(Taggable):
    name = db.StringProperty(required=True)
    slug = SlugProperty(name)
    description = db.TextProperty(required=True)
    live = db.BooleanProperty(required=True)
    promoted = db.BooleanProperty(required=True)
    price = db.FloatProperty(required=True)
    unit = db.StringProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    modified = db.DateTimeProperty(required=True, auto_now=True)
    language = db.StringProperty(required=True)
    
    @classmethod
    def get_promoted_product(self, language=None):
        query = self.all().filter('live =', True).filter('promoted =', True)
        if language:
            query.filter('language =', language)
        return query.get()
    
    @classmethod
    def get_products_by_tag(self, tag, language=None):
        query = self.all()
        query.filter('live =', True)
        query.filter('tags IN', [tag])
        if language:
            query.filter('language =', language)
        query.order('-modified')
        return query.fetch(10)
    
    @classmethod
    def get_product_by_slug(self, slug=None, language=None):
        query = self.all().filter('slug =', slug).filter('live =', True)
        if language:
            query.filter('language =', language)
        return query.get()
    
    @classmethod
    def get_latest_products(self, count=10, live=True, language=None):
        query = self.all()
        if live:
            query.filter('live =', live)
        if language:
            query.filter('language =', language)
        query.order('-modified')
        return query.fetch(count)
    
    @classmethod
    def get_product_list(self, products=None):
        if products is None:
            return []
        result = self.get_by_id(products)
        return result


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
    items = db.StringProperty(required=True)
    user = db.ReferenceProperty(User, required=True)
    comment = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    delivered = db.BooleanProperty(default=False)
    notified = db.BooleanProperty(default=False)
    delivery_method = db.TextProperty(required=True)
    delivery_address = db.StringProperty()
    delivery_city = db.StringProperty()
    delivery_zip = db.StringProperty()
    delivery_info = db.TextProperty()
    
    @classmethod
    def get_orders_by_user(self, user_key=None):
        query = self.all()
        query.filter('user =', user_key)
        result = query.fetch(10)
        if result is None:
            return []
        
        orders = []
        order_item = {}
        
        for order in result:
            items = make_list_from_string(order.items)
            total = calculate_total_price(items)
            order_item = {
                'products': items,
                'total': total,
                'delivery': self.get_formatted_address(order),
                'posted': order.date,
                'delivered': order.delivered,
            }
            orders.append(order_item)
        logging.warn(orders)
        return orders
    
    @classmethod
    def get_formatted_address(self, order):
        address = "%s-%s %s" % (order.delivery_zip, order.delivery_city, order.delivery_address)
        return address
