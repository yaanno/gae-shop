# -*- coding: utf-8 -*-
"""
    forms
    ~~~~

    Order form classes.

"""
from tipfy.ext.wtforms import Form, fields, validators
from tipfy.ext.i18n import gettext as _


REQUIRED = validators.required()

class OrderForm(Form):
    delivery_method = fields.RadioField(
        label=_('Delivery Method'),
        description=_('Chose your preferred delivery method.'),
        choices=[('pickup', _('Pick up')), ('box', _('Box delivery'))], 
        validators=[REQUIRED])
    delivery_address = fields.TextField(
        label=_('Address'),
        description=_('Eg. Clark Adam ter 14.'))
    delivery_city = fields.TextField(
        label=_('City'),
        description=_('Eg. Budapest'))
    delivery_zip = fields.TextField(
        label=_('Zip Code'),
        description=_('Eg. 1123'))
    delivery_info = fields.TextAreaField(
        label=_('Other Information'),
        description=_('Notes on Your order or the delivery.'))
    comment = fields.TextAreaField(
        label=_('Comment'),
        description=_('Additional notes.'))


