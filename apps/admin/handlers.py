# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Administration Application Handlers

"""
from tipfy import Response, cached_property, redirect
from tipfy.ext.i18n import gettext as _
from tipfy.ext.auth import admin_required

from forms import BlogPostForm, ProductForm
from apps.user.handlers import AuthHandler
from apps.blog.models import BlogPost
from apps.shop.models import Product


class BaseHandler(AuthHandler):
    pass


class AdminIndexHandler(BaseHandler):
    """Main view for Admin"""
    @admin_required
    def get(self, **kwargs):
        context = {}
        return self.render_response('admin/index.html', **context)


class ShopIndexHandler(BaseHandler):
    @admin_required
    def get(self, **kwargs):
        products = Product.all().order('-modified')
        result = products.fetch(10)
        context = {
            'products': result,
        }
        return self.render_response('admin/shop/index.html', **context)


class ProductsIndexHandler(BaseHandler):
    @admin_required
    def get(self, **kwargs):
        products = Product.get_latest_products(10, False)
        context = {
            'products': products,
        }
        return self.render_response('admin/product/index.html', **context)


class ProductHandler(BaseHandler):
    @admin_required
    def get(self, product_id=None, **kwargs):
        """Return a product to edit or an empty form to create"""
        template = 'admin/product/new.html'
        context = {
            'form': self.form,
        }
        # render edit form
        if product_id is not None:
            product = Product.get_by_id(product_id)
            if product:
                self.form = ProductForm(obj=product)
                self.form.tags.data = ', '.join(product.tags)
                context.update({ 'form': self.form })
                template = 'admin/product/edit.html'
            else:
                return redirect('/admin/shop/')
        # render new form
        return self.render_response(template, **context)
    
    @admin_required
    def post(self, product_id=None, **kwargs):
        """Handle submitted form data"""
        # validate form
        if self.form.validate():
            name = self.form.name.data
            description = self.form.description.data
            price = self.form.price.data
            unit = self.form.unit.data
            live = self.form.live.data
            tags = self.form.tags.data
            if tags is not None:
                tags = [tag.strip() for tag in tags.split(',') if tag != '']
            # save edit form
            if product_id:
                product = Product.get_by_id(product_id)
                product.name = name
                product.description = description
                product.price = price
                product.unit = unit
                product.live = live
                product.tags = tags
            # save new form
            else:
                product = Product(name=name, description=description, price=price, unit=unit, live=live, tags=tags)
            if product.put():
                return redirect('/admin/shop/products/')
        return self.get(**kwargs)
        
    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return ProductForm(self.request)


class BlogIndexHandler(BaseHandler):
    """Return date ordered blog posts"""
    @admin_required
    def get(self, **kwargs):
        posts = BlogPost.all().order('-modified')
        result = posts.fetch(10)
        context = {
            'posts': result,
        }
        return self.render_response('admin/blog/index.html', **context)


class BlogPostHandler(BaseHandler):
    """Manage individual blog posts"""
    @admin_required
    def get(self, post_id=None, **kwargs):
        """Return a post to edit or an empty form to create"""
        template = 'admin/blog/new.html'
        context = {
            'form': self.form,
        }
        # render edit
        if post_id is not None:
            post = BlogPost.get_by_id(post_id)
            if post:
                self.form = BlogPostForm(obj=post)
                self.form.tags.data = ', '.join(post.tags)
                context.update({ 'form': self.form })
                template = 'admin/blog/edit.html'
            else:
                return redirect('admin/blog/')
        # render new
        return self.render_response(template, **context)
    
    @admin_required
    def post(self, post_id=None, **kwargs):
        """Handle submitted form data"""
        # validate form
        if self.form.validate():
            title = self.form.title.data
            lead = self.form.lead.data
            content = self.form.content.data
            live = self.form.live.data
            tags = self.form.tags.data
            if tags is not None:
                tags = [tag.strip() for tag in tags.split(',') if tag != '']
            # saving edited
            if post_id:
                post = BlogPost.get_by_id(post_id)
                post.title = title
                post.lead = lead
                post.content = content
                post.live = live
                post.tags = tags
            # creating new
            else:
                post = BlogPost(title=title, lead=lead, content=content, live=live, tags=tags)
            if post.put():
                return redirect('admin/blog')
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return BlogPostForm(self.request)

