# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Feed Handlers

"""
import logging

from tipfy import RequestHandler
from tipfy.ext.jinja2 import render_response
import tipfy.ext.i18n as i18n

from apps.blog.models import BlogPost
from apps.shop.models import Product

class BaseHandler(RequestHandler):
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class BlogFeedHandler(BaseHandler):
    
    def get(self, tag=None, **kwargs):
        language = self.get_locale()
        if tag is None:
            posts = BlogPost.get_latest_posts(10, language=language)
        else:
            posts = BlogPost.get_posts_by_tag(tag, language=language)
        context = {
            'posts': posts,
            'tag': tag
        }
        return render_response('feed/blog.xml', **context)


class ProductFeedHandler(BaseHandler):
    
    def get(self, tag=None, **kwargs):
        language = self.get_locale()
        if tag is None:
            products = Product.get_latest_products(10, language=language)
        else:
            products = Product.get_products_by_tag(tag, language=language)
        context = {
            'products': products,
            'tag': tag
        }
        return render_response('feed/product.xml', **context)