# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'tipfy.ext.i18n.I18nMiddleware',
    ],
    # Enable the Hello, World! app example.
    'apps_installed': [
        'apps.blog',
        'apps.admin',
        'apps.pages',
        'apps.shop',
    ],
    'locale': 'en_US',
}