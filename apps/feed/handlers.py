# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    User Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response

from apps.blog.models import BlogPost
from apps.shop.models import Product

class BlogFeedHandler(RequestHandler):
    
    def get(self, tag=None, **kwargs):
        if tag is None:
            posts = BlogPost.get_latest_posts(10)
        else:
            posts = BlogPost.get_posts_by_tag(tag)
        context = {
            'posts': posts,
            'tag': tag
        }
        return render_response('feed/blog.xml', **context)


class ProductFeedHandler(RequestHandler):
    
    def get(self, tag=None, **kwargs):
        if tag is None:
            products = Product.get_latest_products(10)
        else:
            products = Product.get_products_by_tag(tag)
        context = {
            'products': products,
            'tag': tag
        }
        return render_response('feed/product.xml', **context)