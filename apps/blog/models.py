# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~

    Blog Application Models

"""
from datetime import datetime
import calendar

from google.appengine.ext import db
from tipfy.ext.db import SlugProperty

from apps.tagging.models import Taggable

class BlogPost(Taggable):
    """Model for Blog posts"""
    title = db.StringProperty(required=True)
    slug = SlugProperty(title)
    lead = db.TextProperty(required=True)
    content = db.TextProperty(required=True)
    live = db.BooleanProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)
    modified = db.DateTimeProperty(required=True, auto_now=True)
    
    @classmethod
    def get_posts_by_tag(self, tag):
        query = self.all()
        query.filter('live =', True)
        query.filter('tags IN', [tag])
        query.order('-modified')
        return query.fetch(10)
    
    @classmethod
    def get_latest_posts(self, count=10):
        """Return posts"""
        query = self.all().filter('live =', True).order('-modified')
        return query.fetch(count)
    
    @classmethod
    def get_post_by_slug(self, slug=None):
        """Return a post by slug given"""
        query = self.all().filter('slug =', slug).filter('live =', True)
        return query.get()
    
    @classmethod
    def get_posts_by_date(self, year=None, month=None, day=None):
        """Return posts by date given"""
        # prepare dates for filtering
        start_month = end_month = month
        start_day = end_day = day
        start_year = end_year = year
        if year is None:
            start_year = 2009
            end_year = datetime.now().year
        if month is None:
            start_month = 01
            end_month = 12
        if day is None:
            start_day = 01
            end_day = calendar.mdays[end_month]
        
        start_date = datetime(start_year, start_month, start_day)
        end_date = datetime(end_year, end_month, end_day, 23, 59, 59)
        # run query
        query = self.all()
        query.filter('created >=', start_date)
        query.filter('created <=', end_date)
        query.filter('live =', True)
        query.order('-created')
        return query.fetch(10)