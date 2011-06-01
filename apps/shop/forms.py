# -*- coding: utf-8 -*-
"""
    forms
    ~~~~

    Order form classes.

"""
import logging


from tipfy.ext.wtforms import Form, fields, validators
from tipfy.ext.i18n import gettext as _


REQUIRED = validators.required()

class OrderForm(Form):
    delivery_method = fields.RadioField(
        label=_('Delivery Method'),
        description=_('Chose your preferred delivery method.'),
        choices=[('pickup', _('Pick up')), ('box', _('Delivery'))],
        validators=[REQUIRED])
    delivery_area = fields.HiddenField(
        label=''
    )
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
    
    def validate(self):
        if self._validate():
            return True
        else:
            
            return False
    
    def _validate(self):
        if self.delivery_method.data == 'box':
            required = _('This field is required')
            logging.debug(self.delivery_area.data)
            if self.delivery_area.data == '':
                self.delivery_area.errors = ['%s' % required]
            if self.delivery_address.data == '':
                self.delivery_address.errors = ['%s' % required]
            if self.delivery_city.data == '':
                self.delivery_city.errors = ['%s' % required]
            if self.delivery_zip.data == '':
                self.delivery_zip.errors = ['%s' % required]
        if len(self.errors) > 0:
            return False
        else:
            return True


