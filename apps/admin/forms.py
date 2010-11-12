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


class ProductForm(Form):
    name = fields.TextField(
        label=_('Name'),
        description=_('The name of the product'),
        validators=[validators.Required()])
    description = fields.TextAreaField(
        label=_('Description'),
        description=_('A few words about the product'),
        validators=[validators.Required()])
    price = fields.FloatField(
        label = _('Price'),
        description = _('The price of the product'),
        validators=[validators.Required()])
    unit = fields.SelectField(
        label = _('Unit'),
        description = _('The unit of the product'),
        choices = [('piece', _('Piece')), ('gram', _('Gram')), ('pack', _('Pack'))],
        validators=[validators.Required()])
    live = fields.BooleanField(
        label=_('Set live'),
        default=True,
        description=_('Live products will appear immediately'))
    tags = fields.TextField(
        label=_('Tags'),
        description=_('List of tags, separated by comma (,)'))


