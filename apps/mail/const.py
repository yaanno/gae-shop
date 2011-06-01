# -*- coding: utf-8 -*-
"""
    urls
    ~~~~~~~~

    Mailer Constants

"""
from tipfy.ext.i18n import gettext as _


SHOP = "peti@lumenkave.hu"
SENDER = "noreply@lumenkave.hu"
REPLY_TO = "noreply@lumenkave.hu"
SUBJECT_ORDER = _("Order from Lumen Kave")
SUBJECT_REGISTRATION = _("Registration at Lumen Kave")

__all__ = ["SENDER", "REPLY_TO", "SUBJECT_ORDER", "SUBJECT_REGISTRATION", "SHOP"]