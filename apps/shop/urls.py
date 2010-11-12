# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Shop application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.shop.handlers.', [
            Rule('/shop/', endpoint='shop/index', handler='ShopIndexHandler'),
            Rule('/shop/product/<slug>/', endpoint='shop/product', handler='ProductHandler'),
            Rule('/shop/tag/<tag>/', endpoint='shop/tag', handler='ShopTagListHandler'),
        ]),
    ]

    return rules
