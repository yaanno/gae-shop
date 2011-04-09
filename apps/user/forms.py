# -*- coding: utf-8 -*-
"""
    forms
    ~~~~

    Authentication form classes.

"""
from tipfy.ext.wtforms import Form, fields, validators
from tipfy.ext.i18n import gettext as _


REQUIRED = validators.required()

class LoginForm(Form):
    username = fields.TextField(_('Username'), validators=[REQUIRED])
    password = fields.PasswordField(_('Password'), validators=[REQUIRED])
    remember = fields.BooleanField(_('Keep me signed in'))


class RegistrationForm(Form):
    username = fields.TextField(_('Username'), validators=[REQUIRED])
    password = fields.PasswordField(_('Password'), validators=[REQUIRED])
    password_confirm = fields.PasswordField(_('Confirm the password'), validators=[REQUIRED])
    email = fields.TextField(_('E-mail'), validators=[REQUIRED])
    email_confirm = fields.TextField(_('E-mail confirmation'), validators=[REQUIRED])


class SignupForm(Form):
    nickname = fields.TextField(_('Username'), validators=[REQUIRED])