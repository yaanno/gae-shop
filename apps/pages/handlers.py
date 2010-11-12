# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Page Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response


class NotFoundHandler(RequestHandler):
    def get(self):
        return Response('Page not found')


class WelcomePageHandler(RequestHandler):
    def get(self, **kwargs):
        context = {}
        return render_response('pages/welcome.html', **context)
        