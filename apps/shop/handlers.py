# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Shop Application Handlers

"""
import logging

from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response
from tipfy.ext.session import SessionMixin, SessionMiddleware

from apps.user.handlers import AuthHandler
from models import Product
from helpers import get_cart_content

class BaseHandler(AuthHandler):
    pass


class ShopIndexHandler(BaseHandler):
    def get(self, **kwargs):
        cart = get_cart_content()
        products = Product.get_latest_products()
        context = {
            'products': products,
            'cart': cart,
        }
        return self.render_response('shop/index.html', **context)


class ProductHandler(BaseHandler):
    def get(self, slug=None, **kwargs):
        product = Product.get_product_by_slug(slug)
        if product is not None:
            context = {
                'product': product
            }
            return self.render_response('shop/show.html', **context)
        else:
            return redirect_to('notfound')


class ShopTagListHandler(BaseHandler):
    def get(self, tag=None, **kwargs):
        products = Product.get_products_by_tag(tag)
        context = {
            'products': products,
            'tag': tag
        }
        return self.render_response('shop/by_tag.html', **context)


class CartHandler(BaseHandler):
    def get(self, **kwargs):
        return Response('cart goes here')