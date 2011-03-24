# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Page Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response
import tipfy.ext.i18n as i18n

from apps.user.handlers import AuthHandler
from apps.shop.models import Product
from apps.blog.models import BlogPost


class BaseHandler(AuthHandler):
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class NotFoundHandler(BaseHandler):
    def get(self):
        return self.render_response('pages/404.html')


class WelcomePageHandler(BaseHandler):
    def get(self, **kwargs):
        language = self.get_locale()
        products = Product.get_latest_products(3, language=language)
        posts = BlogPost.get_latest_posts(5, language=language)
        context = {
            'products': products,
            'posts': posts,
        }
        return self.render_response('pages/welcome.html', **context)


