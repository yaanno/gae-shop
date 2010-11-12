# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Shop Application Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response


class ShopIndexHandler(RequestHandler):
    def get(self, **kwargs):
        context = {}
        return render_response('shop/index.html', **context)


class ShopTagListHandler(RequestHandler):
    def get(self, **kwargs):
        context = {}
        return render_response('shop/tags.html', **context)