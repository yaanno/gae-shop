# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Feed application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.feed.handlers.', [
            Rule('/feed/blog/', endpoint='feed/blog', handler='BlogFeedHandler'),
            Rule('/feed/blog/tag/<tag>/', endpoint='feed/blog', handler='BlogFeedHandler'),
            Rule('/feed/product/', endpoint='feed/shop', handler='ProductFeedHandler'),
            Rule('/feed/product/tag/<tag>/', endpoint='feed/shop', handler='ProductFeedHandler'),
        ]),
    ]
    
    return rules
