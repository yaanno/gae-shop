# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    Blog Application Handlers

"""
from tipfy import RequestHandler, Response, redirect_to
from tipfy.ext.jinja2 import render_response
import tipfy.ext.i18n as i18n

from apps.user.handlers import AuthHandler
from models import BlogPost
from helpers import dateformatter, group_by_date


class BaseHandler(AuthHandler):
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()


class BlogIndexHandler(BaseHandler):
    """Return date ordered blog posts"""
    def get(self, **kwargs):
        language = self.get_locale()
        posts = BlogPost.get_latest_posts(10, language=language)
        context = {
            'posts': posts,
        }
        return self.render_response('blog/index.html', **context)


class BlogPostHandler(BaseHandler):
    """Return an individual blog post"""
    def get(self, year=None, month=None, day=None, slug=None):
        language = self.get_locale()
        post = BlogPost.get_post_by_slug(slug, language=language)
        if post is not None:
            context = {
                'post': post
            }
            return self.render_response('blog/show.html', **context)
        else:
            return redirect_to('notfound')


class BlogArchiveHandler(BaseHandler):
    """Return date ordered blog posts depending on archive filters"""
    def get(self, year=None, month=None, day=None):
        language = self.get_locale()
        posts = BlogPost.get_posts_by_date(year, month, day, language=language)
        # date = dateformatter(year, month, day)
        if year is None:
            posts = group_by_date(posts)
        if posts is not None:
            context = {
                'posts': posts,
            }
            return self.render_response('blog/archive.html', **context)
        else:
            return redirect_to('notfound')


class BlogTagListHandler(BaseHandler):
    """Return list of posts by tag name"""
    def get(self, tag=None):
        language = self.get_locale()
        posts = BlogPost.get_posts_by_tag(tag, language=language)
        context = {
            'posts': posts,
            'tag': tag,
        }
        if len(posts) > 0:
            return self.render_response('blog/archive.html', **context)
        else:
            return redirect_to('notfound')


