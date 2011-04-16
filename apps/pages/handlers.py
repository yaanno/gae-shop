# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Page Handlers

"""
import logging

from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response
import tipfy.ext.i18n as i18n

from apps.user.handlers import AuthHandler
from apps.shop.models import Product
from apps.blog.models import BlogPost
from apps.pages.models import Page


class BaseHandler(AuthHandler):
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class ErrorHandler(BaseHandler):
    def get(self, error_code=None):
        language = self.get_locale()
        context = {
            'language': language,
        }
        code = '404'
        if error_code:
            code = str(error_code)
        return self.render_response('pages/%s.html' % code, **context)


class WelcomePageHandler(BaseHandler):
    
    def get(self, **kwargs):
        language = self.get_locale()
        products = Product.get_latest_products(3, language=language)
        posts = BlogPost.get_latest_posts(5, language=language)
        context = {
            'products': products,
            'posts': posts,
            'language': language,
        }
        return self.render_response('pages/welcome.html', **context)


class PageHandler(BaseHandler):
    
    def get(self, slug=None, **kwargs):
        language = self.get_locale()
        page = Page.get_page_by_slug(slug, language=language)
        context = {
            'page': page,
            'language': language,
        }
        if page is None:
            return self.redirect_to('notfound')
        return self.render_response('pages/show.html', **context)