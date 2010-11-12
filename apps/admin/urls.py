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
        HandlerPrefix('apps.admin.handlers.', [
            Rule('/admin/', endpoint='admin/index', handler='AdminIndexHandler'),
            Rule('/admin/blog/', endpoint='admin/blog/index', handler='BlogIndexHandler'),
            Rule('/admin/blog/new/', endpoint='admin/blog/new', handler='BlogPostHandler'),
            Rule('/admin/blog/edit/<int:post_id>/', endpoint='admin/blog/edit', handler='BlogPostHandler'),
            Rule('/admin/shop/', endpoint='admin/shop/index', handler='ShopIndexHandler'),
            Rule('/admin/product/new/', endpoint='admin/product/new', handler='ProductHandler'),
        ]),
    ]

    return rules
