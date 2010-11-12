# -*- coding: utf-8 -*-
"""
    helpers
    ~~~~~~~~

    Blog Application Helpers

"""
from datetime import date

from tipfy.ext.i18n import format_date


def dateformatter(year=None, month=None, day=None):
    """Return a formatted datetime object"""
    old = date(year, month, day)
    return format_date(old, 'long')

def group_by_date(posts):
    """Return a dict of posts grouped by year, month"""
    """
        posts = [
            {'2009': [
                {'01': [post, post]},
                {'05': [post]},
            ]},
            {'2010': [
                {'10': [post, post]},
                {'12': [post]},
            ]}
        ]
    """
    return posts
    