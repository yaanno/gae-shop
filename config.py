# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2010 Janos Hardi.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
        'tipfy.ext.i18n.I18nMiddleware',
    ],
    'apps_installed': [
        'apps.blog',
        'apps.admin',
        'apps.pages',
        'apps.shop',
    ],
    'locale': ['hu_HU', 'en_US'],
}

config['tipfy.ext.session'] = {
    'secret_key': 'ROtbnD8SEjPbUiOgcanANFE6eKKulwMExPM60rM7UMvKBBjAmFjx396r0YgCfyN',
}
