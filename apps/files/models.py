# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    File (Blob) Models

"""
import logging

from google.appengine.ext import db, blobstore


class File(db.Model):
    title = db.StringProperty(required=True)
    file_data = blobstore.BlobReferenceProperty(required=True)
    
    @classmethod
    def get_latest_files(self, format=None, count=10):
        query = self.all()
        if format is not None:
            query.filter('content_type =', format)
        results = query.fetch(count)
        return results