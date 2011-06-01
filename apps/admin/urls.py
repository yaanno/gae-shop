# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions for the Admin application.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Administration application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.admin.handlers.', [
            # admin main
            Rule('/admin/', endpoint='admin/index', handler='AdminIndexHandler'),
            # admin blog
            Rule('/admin/blog/', endpoint='admin/blog/index', handler='BlogIndexHandler'),
            Rule('/admin/blog/new/', endpoint='admin/blog/new', handler='BlogPostHandler'),
            Rule('/admin/blog/edit/<int:post_id>/', endpoint='admin/blog/edit', handler='BlogPostHandler'),
            # admin offers
            Rule('/admin/daily/', endpoint='admin/daily/index', handler='OfferIndexHandler'),
            Rule('/admin/daily/new/', endpoint='admin/daily/new', handler='OfferHandler'),
            Rule('/admin/daily/edit/<int:offer_id>/', endpoint='admin/daily/edit', handler='OfferHandler'),
            # admin pages
            Rule('/admin/page/', endpoint='admin/page/index', handler='PageIndexHandler'),
            Rule('/admin/page/new/', endpoint='admin/page/new', handler='PageHandler'),
            Rule('/admin/page/edit/<int:page_id>/', endpoint='admin/page/edit', handler='PageHandler'),
            # admin shop
            Rule('/admin/shop/', endpoint='admin/shop/index', handler='ShopIndexHandler'),
            # admin products
            Rule('/admin/shop/products/', endpoint='admin/products/index', handler='ProductsIndexHandler'),
            Rule('/admin/shop/products/new/', endpoint='admin/products/new', handler='ProductHandler'),
            Rule('/admin/shop/products/edit/<int:product_id>/', endpoint='admin/products/edit', handler='ProductHandler'),
            # admin orders
            Rule('/admin/shop/orders/', endpoint='admin/orders/index', handler='OrdersIndexHandler'),
            Rule('/admin/shop/orders/<int:order_id>/', endpoint='admin/orders/edit', handler='OrderStateHandler'),
            # files
            Rule('/admin/files/', endpoint='admin/files/index', handler='FileIndexHandler'),
            Rule('/admin/files/new/', endpoint='blobstore/upload', handler='FileHandler'),
        ]),
    ]

    return rules
