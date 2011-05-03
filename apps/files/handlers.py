# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    File Upload Handlers

"""
import logging

from google.appengine.ext import blobstore

from tipfy import Response, RequestHandler
from tipfy.ext.blobstore import BlobstoreDownloadMixin

from models import File


class FileServe(RequestHandler, BlobstoreDownloadMixin):
    
    def get(self, **kwargs):
        logging.warn(kwargs.get('resource'))
        blob_info = blobstore.BlobInfo.get(kwargs.get('resource'))
        
        return self.send_blob(blob_info)


class ImageBrowser(RequestHandler):
    
    def get(self, **kwargs):
        format = None
        images = File.get_latest_files(format)
        logging.warn(images) # file obj
        
        '''
        format: var tinyMCEImageList = new Array([
            ['title', 'filename'],
            ['title', 'filename']
        ])
        '''
        image_list = []
        for image in images:
            logging.warn(image.file_data)
            logging.warn(dir(image.file_data))
            image_list.append([str(image.title), str("file/%s" % image.file_data.key())])
        
        image_list = "var tinyMCEImageList = %s" % str(image_list)
        
        return Response(image_list, mimetype='application/javascript')