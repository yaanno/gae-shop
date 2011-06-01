# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Shop Application Handlers

"""
import logging

from google.appengine.api import taskqueue

from django.utils import simplejson as json

from tipfy import redirect_to, render_json_response, cached_property, redirect
import tipfy.ext.i18n as i18n
from tipfy.ext.auth import user_required

from apps.user.handlers import AuthHandler
from models import Product, Order
from forms import OrderForm
from helpers import calculate_total_price, make_list_from_dict

class BaseHandler(AuthHandler):
    
    def get_cart_content(self):
        products = self.session.setdefault('products', [])
        return products
    
    def reset_cart(self):
        products = self.session['products'] = []
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class ShopIndexHandler(BaseHandler):
    def get(self, **kwargs):
        language = self.get_locale()
        products = Product.get_latest_products(language=language)
        context = {
            'products': products,
            'language': language,
            'format_currency': i18n.format_currency,
        }
        return self.render_response('shop/index.html', **context)


class ProductHandler(BaseHandler):
    def get(self, slug=None, **kwargs):
        language = self.get_locale()
        product = Product.get_product_by_slug(slug, language=language)
        if product is not None:
            context = {
                'product': product,
                'language': language,
                'format_currency': i18n.format_currency,
            }
            return self.render_response('shop/show.html', **context)
        else:
            return redirect_to('notfound')


class ShopTagListHandler(BaseHandler):
    def get(self, tag=None, **kwargs):
        language = self.get_locale()
        products = Product.get_products_by_tag(tag)
        context = {
            'products': products,
            'tag': tag,
            'language': language,
            'format_currency': i18n.format_currency,
        }
        return self.render_response('shop/by_tag.html', **context)


class CartHandler(BaseHandler):
    # TODO: finish the update part: add / remove items / counts
    
    def _add_to_cart(self, product_id=None, product_quantity=None, product_name=None, product_price=None, product_unit=None):
        products = self.get_cart_content()
        
        #logging.warn(products)
        
        def do_add_to_cart():
            products.append({
                'product_quantity': product_quantity,
                'product_id': product_id,
                'product_name': product_name,
                'product_price': product_price,
                'product_unit': product_unit,
            })
        
        existing_product = [p for p in products if p['product_id'] == product_id]
        
        if len(existing_product):
            existing_product[0]['product_quantity'] += product_quantity
        else:
            do_add_to_cart()
        
        return products
    
    
    def _update_cart(self):
        pass
    
    
    def get(self, **kwargs):
        products = self.session.get('products')
        language = self.get_locale()
        total = calculate_total_price(products)
        context = {
            'products': products,
            'language': language,
            'format_currency': i18n.format_currency,
            'total': total,
        }
        
        return self.render_response('shop/cart.html', **context)
    
    def put(self,**kwargs):
        products_cart = self.get_cart_content()
        products = self.request.form.keys()
        products = json.loads(products[0])
        
        for product in products['products']:
            logging.warn(product['product_id'])
            match = [p for p in products_cart if p['product_id'] == int(product['product_id'])]
            logging.warn(match)
            
            q = int(product['product_quantity'])
            
            if q == 0:
                products_cart.remove(match[0])
            else:
                match[0]['product_quantity'] = q
        
        context = {}
        if products is not None:
            context = { 'success': True, 'products': products }
        else:
            context = { 'success': False, 'products': [] }
        return render_json_response(context)
    
    
    def post(self, **kwargs):
        product_quantity = self.request.form.get('product_quantity', type=int)
        product_id = self.request.form.get('product_id', type=int)
        
        # check if product exists
        product = Product.get_by_id(product_id)
        product_name = product.name
        product_price = product.price
        product_unit = product.unit
        
        context = {}
        
        if product is not None:
            cart = self._add_to_cart(product_id, product_quantity, product_name, product_price, product_unit)
            context = { 'success': True, 'products': cart }
        else:
            context = { 'success': False, 'products': [] }
        return render_json_response(context)
        


class OrderHandler(BaseHandler):
    
    @user_required
    def get(self, **kwargs):
        user = self.auth_current_user
        products = self.get_cart_content()
        total = calculate_total_price(products)
        context = {
            'user': user,
            'form': self.form,
            'products': products,
            'total': total,
            'format_currency': i18n.format_currency,
        }
        return self.render_response('shop/order.html', **context)
    
    @user_required
    def post(self, **kwargs):
        current_user = self.auth_current_user
        products = self.get_cart_content()
        items = []
        
        if self.form.validate():
            user = current_user
            delivery_method = self.form.delivery_method.data
            delivery_area = self.form.delivery_area.data
            delivery_info = self.form.delivery_info.data
            delivery_address = self.form.delivery_address.data
            delivery_city = self.form.delivery_city.data
            delivery_zip = self.form.delivery_zip.data
            comment = self.form.comment.data
            items = str(products)
            order = Order(items=items, user=user.key(), delivery_method=delivery_method, delivery_address=delivery_address, delivery_city=delivery_city, delivery_zip=delivery_zip, comment=comment, delivery_info=delivery_info, delivery_area=delivery_area)
            
            if order.put():
                url = '/mail/notify/order/'
                order_id = str(order.key().id())
                payload = { 'order_id': order_id }
                task = taskqueue.add(url=url, params=payload)
                return redirect('shop/thankyou')
            
            
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        return OrderForm(self.request)


class PostOrderHandler(BaseHandler):
    
    @user_required
    def get(self, **kwargs):
        self.reset_cart()
        context = {}
        return self.render_response('shop/thankyou.html', **context)