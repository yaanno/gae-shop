# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    File Upload Handlers

"""

from google.appengine.ext import blobstore

from tipfy import Response, RequestHandler
from tipfy.ext.blobstore import BlobstoreDownloadMixin


class FileServe(RequestHandler, BlobstoreDownloadMixin):
    
    def get(self, **kwargs):
        
        blob_info = blobstore.BlobInfo.get(kwargs.get('resource'))
        return self.send_blob(blob_info)