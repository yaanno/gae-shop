# -*- coding: utf-8 -*-
"""
    urls
    ~~~~~~~~

    Mailer Urls

"""

from tipfy import Rule, HandlerPrefix


def get_rules(app):
    rules = [
        HandlerPrefix('apps.mail.handlers.', [
            Rule('/_ah/mail/inbound', endpoint='mail/incoming', handler='IncomingMailHandler'),
            Rule('/mail/send/', endpoint='mail/send', handler='OrderMailHandler'),
            Rule('/mail/verify/<user_key>/', endpoint='mail/verify', handler='VerificationMailHandler'),
        ])
    ]
    return rules