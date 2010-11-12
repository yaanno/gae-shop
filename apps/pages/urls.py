# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Hello, World! application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.pages.handlers.', [
            Rule('/', endpoint='pages/welcome', handler='WelcomePageHandler'),
            Rule('/notfound/', endpoint='notfound', handler='NotFoundHandler'),
        ]),
    ]

    return rules
