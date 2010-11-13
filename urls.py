# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2010 Janos Hardi.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule, import_string


def get_rules(app):
    """Returns a list of URL rules for the application. The list can be
    defined entirely here or in separate ``urls.py`` files.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = []

    for app_module in app.get_config('tipfy', 'apps_installed'):
        try:
            # Load the urls module from the app and extend our rules.
            app_rules = import_string('%s.urls' % app_module)
            rules.extend(app_rules.get_rules(app))
        except ImportError:
            pass

    return rules
