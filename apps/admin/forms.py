# -*- coding: utf-8 -*-
"""
    forms
    ~~~~

    Various form classes.

"""
from tipfy.ext.wtforms import Form, fields, validators
from tipfy.ext.i18n import gettext as _

class BlogPostForm(Form):
    title = fields.TextField(
        label=_('Title'),
        description=_('The title of your blog post'),
        validators=[validators.Required()])
    lead = fields.TextAreaField(
        label=_('Lead'),
        description=_('A limited length lead text for your post'),
        validators=[validators.Required()])
    content = fields.TextAreaField(
        label=_('Content'),
        description=_('The main text for your blog post'),
        validators=[validators.Required()])
    live = fields.BooleanField(
        label=_('Set live'),
        description=_('Live posts will appear immediately'))
    tags = fields.TextField(
        label=_('Tags'),
        description=_('List of tags, separated by comma (,)'))