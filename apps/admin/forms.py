# -*- coding: utf-8 -*-
"""
    forms
    ~~~~

    Various form classes.

"""
from tipfy.ext.wtforms import Form, fields, validators
from tipfy.ext.i18n import gettext as _


class BlogPostForm(Form):
    """Form class for Blog post validation"""
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
        id="post_content",
        validators=[validators.Required()])
    live = fields.BooleanField(
        label=_('Set live'),
        description=_('Live posts will appear immediately'))
    tags = fields.TextField(
        label=_('Tags'),
        description=_('List of tags, separated by comma (,)'))
    language = fields.SelectField(
        label = _('Language'),
        description = _('The site language the post will appear'),
        choices = [('hu_HU', _('Magyar')), ('en_US', _('English'))],
        default = 'hu_HU',
        validators=[validators.Required()])


class OfferForm(Form):
    """Form class for Daily offer validation"""
    title = fields.TextField(
        label=_('Title'),
        description=_('The title of your offer'),
        validators=[validators.Required()])
    intro = fields.TextAreaField(
        label=_('Intro'),
        description=_('A limited length lead text that will appear on the front page'),
        validators=[validators.Required()])
    content = fields.TextAreaField(
        label=_('Content'),
        description=_('The main text for your offer if you intend to make it available as a separate page.'),
        id="offer_content")
    live = fields.BooleanField(
        label=_('Set live'),
        description=_('Live offers will appear immediately'))
    promoted = fields.BooleanField(
        label=_('Promoted'),
        description=_('Promoted offers will appear on the front page.'))
    language = fields.SelectField(
        label = _('Language'),
        description = _('The site language the offer will appear'),
        choices = [('hu_HU', _('Magyar')), ('en_US', _('English'))],
        default = 'hu_HU',
        validators=[validators.Required()])


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
    promoted = fields.BooleanField(
        label=_('Place on the front page'),
        default=False,
        description=_('It will appear on the front page'))
    tags = fields.TextField(
        label=_('Tags'),
        description=_('List of tags, separated by comma (,)'))
    language = fields.SelectField(
        label = _('Language'),
        description = _('The site language the product will appear'),
        choices = [('hu_HU', _('Magyar')), ('en_US', _('English'))],
        default = 'hu_HU',
        validators=[validators.Required()])

class PageForm(Form):
    title = fields.TextField(
        label=_('Title'),
        description=_('The title of the page'),
        validators=[validators.Required()])
    content = fields.TextAreaField(
        label=_('Content'),
        id="page_content",
        description=_('Content of the page'),
        validators=[validators.Required()])
    live = fields.BooleanField(
        label=_('Set live'),
        default=True,
        description=_('Live products will appear immediately'))
    language = fields.SelectField(
        label = _('Language'),
        description = _('The site language the page will appear'),
        choices = [('hu_HU', _('Magyar')), ('en_US', _('English'))],
        default = 'hu_HU',
        validators=[validators.Required()])


class FileForm(Form):
    title = fields.TextField(
        label=_('Title'),
        description=_('The title of the file'),
        validators=[validators.Required()])
    file_data = fields.FileField(
        label=_('File to upload'),
        description=_('Select file to upload'),
        validators=[validators.Required()])

