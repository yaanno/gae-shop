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
    comment = fields.TextAreaField(_('Comment'))
    delivery_method = fields.RadioField(_('Delivery Method'), choices=[('pickup', _('Pick up')), ('box', _('Box delivery'))], validators=[REQUIRED])
    delivery_address = fields.TextField(_('Address'))
    delivery_city = fields.TextField(_('City'))
    delivery_zip = fields.TextField(_('Zip Code'))
    delivery_info = fields.TextAreaField(_('Other Information'))