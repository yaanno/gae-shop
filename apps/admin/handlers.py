# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Administration Application Handlers

"""
import logging

from google.appengine.ext import blobstore

from tipfy import Response, cached_property, redirect, url_for, redirect_to
from tipfy.ext.i18n import gettext as _
from tipfy.ext.auth import admin_required
from tipfy.ext.blobstore import BlobstoreUploadMixin

from forms import BlogPostForm, ProductForm, PageForm, FileForm
from apps.user.handlers import AuthHandler
from apps.blog.models import BlogPost
from apps.shop.models import Product
from apps.pages.models import Page
from apps.files.models import File


class BaseHandler(AuthHandler):
    pass


class AdminIndexHandler(BaseHandler):
    """Main view for Admin"""
    @admin_required
    def get(self, **kwargs):
        context = {}
        return self.render_response('admin/index.html', **context)


class FileIndexHandler(BaseHandler):
    
    @admin_required
    def get(self, **kwargs):
        
        files = File.get_latest_files(10)
        context = {
            'files': files
        }
        return self.render_response('admin/files/index.html', **context)


class FileHandler(BaseHandler, BlobstoreUploadMixin):
    
    @admin_required
    def get(self, file_key=None, **kwargs):
        template = 'admin/files/new.html'
        context = {
            'form': self.form,
            'upload_url': blobstore.create_upload_url(url_for('blobstore/upload'))
        }
        return self.render_response(template, **context)

    @admin_required
    def post(self, **kwargs):
        
        if self.form.validate():
            title = self.form.title.data
            file_data = self.form.file_data.data
            
            uploaded_files = self.get_uploads('file_data')
            blob_info = uploaded_files[0]
            logging.warn(blob_info)
            new_file = File(title=title, file_data=blob_info.key())
            # checking the file
            response = redirect_to('admin/files/index')
            if new_file.put():
                response.data = ''
                return response
            
        return self.get(**kwargs)

    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return FileForm(self.request)


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
            promoted = self.form.promoted.data
            tags = self.form.tags.data
            language = self.form.language.data
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
                product.promoted = promoted
                product.tags = tags
                product.language = language
            # save new form
            else:
                product = Product(name=name, description=description, price=price, unit=unit, live=live, promoted=promoted, tags=tags, language=language)
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
            language = self.form.language.data
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
                post.language = language
            # creating new
            else:
                post = BlogPost(title=title, lead=lead, content=content, live=live, tags=tags, language=language)
            if post.put():
                return redirect('admin/blog')
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return BlogPostForm(self.request)


class PageIndexHandler(BaseHandler):
    @admin_required
    def get(self, **kwargs):
        pages = Page.all()
        result = pages.fetch(20)
        context = {
            'pages': result,
        }
        return self.render_response('admin/page/index.html', **context)


class PageHandler(BaseHandler):
    """Manage individual pages"""
    
    @admin_required
    def get(self, page_id=None, **kwargs):
        """Return a page to edit or an empty form to create"""
        template = 'admin/page/new.html'
        context = {
            'form': self.form,
        }
        # render edit
        if page_id is not None:
            page = Page.get_by_id(page_id)
            if page:
                self.form = PageForm(obj=page)
                context.update({ 'form': self.form })
                template = 'admin/page/edit.html'
            else:
                return redirect('admin/page/')
        # render new
        return self.render_response(template, **context)

    @admin_required
    def post(self, page_id=None, **kwargs):
        """Handle submitted form data"""
        # validate form
        if self.form.validate():
            title = self.form.title.data
            content = self.form.content.data
            live = self.form.live.data
            language = self.form.language.data
            # saving edited
            if page_id:
                page = Page.get_by_id(page_id)
                page.title = title
                page.content = content
                page.live = live
                page.language = language
            # creating new
            else:
                page = Page(title=title, content=content, live=live, language=language)
            if page.put():
                return redirect('admin/page')
        return self.get(**kwargs)

    @cached_property
    def form(self):
        """Form instance as cached_property"""
        return PageForm(self.request)