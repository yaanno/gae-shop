# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Page Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response

from apps.user.handlers import AuthHandler
from apps.shop.models import Product
from apps.blog.models import BlogPost


class BaseHandler(AuthHandler):
    pass


class NotFoundHandler(BaseHandler):
    def get(self):
        return self.render_response('pages/404.html')


class WelcomePageHandler(BaseHandler):
    def get(self, **kwargs):
        products = Product.get_latest_products(3)
        posts = BlogPost.get_latest_posts(5)
        context = {
            'products': products,
            'posts': posts,
        }
        return self.render_response('pages/welcome.html', **context)
        