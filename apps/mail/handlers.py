# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Mailer Handlers

"""

import logging

from google.appengine.api import mail

from tipfy import Response
from tipfy.ext.jinja2 import render_template
from tipfy.ext.i18n import gettext as _
import tipfy.ext.i18n as i18n

from tipfy.ext.auth.model import User

from const import *

from apps.user.handlers import AuthHandler
from apps.user.models import Profile
from apps.shop.models import Order


class MailHandler(AuthHandler):
    pass


class OrderMailHandler(MailHandler, AuthHandler):
    
    def get(self, **kwargs):
        '''
        Send e-mail to user ordered a delivery and the admin
        '''
        user = self.auth_current_user # todo: use real user
        order = Order.get_orders_by_user(user)
        context = {
            'order': order,
            'username': user.username,
            'format_currency': i18n.format_currency,
        }
        logging.warn(context)
        body = render_template('mail/order.html', **context)
        message = mail.EmailMessage()
        
        message.to = user.email
        message.body = body
        message.subject = SUBJECT_ORDER
        message.sender = SENDER
        message.reply_to = REPLY_TO
        message.send()
        
        return Response(body)


class VerificationMailHandler(MailHandler):

    def get(self, user_key=None):
        '''
        Send e-mail to user ordered a delivery and the admin
        '''
        user = User.get(user_key)
        logging.warn(user)
        profile = Profile.all().filter('user =', user.key()).get()
        
        if profile.verified:
            return Response('already verified')
        
        context = {
            'user': user,
            'profile': profile,
        }
        
        body = render_template('mail/verify.html', **context)
        message = mail.EmailMessage()

        message.to = user.email
        message.body = body
        message.subject = SUBJECT_REGISTRATION
        message.sender = SENDER
        message.reply_to = REPLY_TO
        message.send()
        
        return Response(body)


