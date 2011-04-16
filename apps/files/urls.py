# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions for the Admin application.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Files application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.files.handlers.', [
            Rule('/file/<resource>', endpoint='blobstore/serve', handler='FileServe'),
        ]),
    ]

    return rules
