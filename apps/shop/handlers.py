# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Shop Application Handlers

"""
import logging

from tipfy import RequestHandler, Response, redirect_to, render_json_response
from tipfy.ext.jinja2 import render_response
from tipfy.ext.session import SessionMixin, SessionMiddleware
import tipfy.ext.i18n as i18n

from apps.user.handlers import AuthHandler
from models import Product

class BaseHandler(AuthHandler):
    
    def get_cart_content(self):
        products = self.session.setdefault('products', [])
        return products
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class ShopIndexHandler(BaseHandler):
    def get(self, **kwargs):
        language = self.get_locale()
        cart = self.get_cart_content()
        products = Product.get_latest_products(language=language)
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
    
    def _add_to_cart(self, product_id=None, product_quantity=None, product_name=None):
        products = self.get_cart_content()
        products.append({
            'product_quantity': product_quantity,
            'product_id': product_id,
            'product_name': product_name,
        })
        
        return products


    def get(self, **kwargs):
        products = self.session.get('products')
        return Response('cart: %s' % products)
    
    def post(self, **kwargs):
        product_quantity = self.request.form.get('product_quantity', type=int)
        product_id = self.request.form.get('product_id', type=int)
        
        # check if product exists
        product = Product.get_by_id(product_id)
        product_name = product.name
        
        context = {}
        
        if product is not None:
            cart = self._add_to_cart(product_id, product_quantity, product_name)
            context = { 'success': True, 'products': cart }
        else:
            context = { 'success': False, 'products': [] }
        return render_json_response(context)

