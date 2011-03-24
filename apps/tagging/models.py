# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Tagging Application Models

"""

"""
    Tagging has:
    Tag:
        - title
        - slug
    Taggable:
        - slug
"""
from google.appengine.ext import db
from google.appengine.ext.db import polymodel


class Taggable(polymodel.PolyModel):
    tags = db.StringListProperty()