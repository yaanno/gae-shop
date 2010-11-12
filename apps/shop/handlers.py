# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Shop Application Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response

from models import Product

class ShopIndexHandler(RequestHandler):
    def get(self, **kwargs):
        products = Product.get_latest_products()
        context = {
            'products': products
        }
        return render_response('shop/index.html', **context)


class ProductHandler(RequestHandler):
    def get(self, slug=None, **kwargs):
        product = Product.get_product_by_slug(slug)
        if product is not None:
            context = {
                'product': product
            }
            return render_response('shop/show.html', **context)
        else:
            return redirect_to('notfound')


class ShopTagListHandler(RequestHandler):
    def get(self, tag=None, **kwargs):
        products = Product.get_products_by_tag(tag)
        context = {
            'products': products
        }
        return render_response('shop/index.html', **context)


