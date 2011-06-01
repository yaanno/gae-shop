# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Daily Offer Handlers

"""
import logging

import tipfy.ext.i18n as i18n

from apps.user.handlers import AuthHandler
from apps.daily.models import Offer


class BaseHandler(AuthHandler):
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class OfferHandler(BaseHandler):
    
    def get(self, slug=None, **kwargs):
        language = self.get_locale()
        page = Offer.get_by_slug(slug, language=language)
        context = {
            'offer': offer,
            'language': language,
        }
        if page is None:
            return self.redirect_to('notfound')
        return self.render_response('daily/show.html', **context)

