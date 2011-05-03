# -*- coding: utf-8 -*-
"""
    handlers
    ~~~~~~~~

    User Handlers

"""
import logging

from google.appengine.api import taskqueue

from tipfy import RequestHandler, Response, abort, cached_property, redirect, url_for, redirect_to
from tipfy.ext.auth import MultiAuthMixin, login_required, user_required
from tipfy.ext.auth.facebook import FacebookMixin
from tipfy.ext.auth.google import GoogleMixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.jinja2 import Jinja2Mixin
from tipfy.ext.i18n import gettext as _
import tipfy.ext.i18n as i18n

from apps.shop.models import Order

from forms import LoginForm, RegistrationForm, SignupForm
from models import Profile


class AuthHandler(RequestHandler, MultiAuthMixin, Jinja2Mixin, AllSessionMixins):
    middleware = [SessionMiddleware]
    
    @staticmethod
    def get_locale():
        return i18n.get_locale()
    
    def render_response(self, filename, **kwargs):
        auth_session = None
        if 'id' in self.auth_session:
            auth_session = self.auth_session
        
        language = self.get_locale()
        
        self.request.context.update({
            'auth_session': auth_session,
            'current_user': self.auth_current_user,
            'login_url': self.auth_login_url(),
            'logout_url': self.auth_logout_url(),
            'current_url': self.request.url,
            'language': language,
            'format_currency': i18n.format_currency,
        })
        if self.messages:
            self.request.context.update({
                'messages': self.messages
            })
        
        return super(AuthHandler, self).render_response(filename, **kwargs)
    
    def redirect_path(self, default='/'):
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = self.request.args.get('continue', '/')
        
        if not url.startswith('/'):
            url = default
        
        return url
    
    def _on_auth_redirect(self):
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = ('/')
        
        if not self.auth_current_user:
            url = self.auth_signup_url()
        
        return redirect(url)


class LoginHandler(AuthHandler):
    
    def get(self, **kwargs):
        redirect_url = self.redirect_path()
        if self.auth_current_user:
            return redirect(redirect_url)
        opts = {'continue': self.redirect_path()}
        context = {
            'form': self.form,
            'facebook_login_url': url_for('auth/facebook', **opts),
            'google_login_url': url_for('auth/google', **opts),
        }
        return self.render_response('user/login.html', **context)
    
    def post(self, **kwargs):
        redirect_url = self.redirect_path()
        if self.auth_current_user:
            return redirect(redirect_url)
        
        if self.form.validate():
            username = self.form.username.data
            password = self.form.password.data
            remember = self.form.remember.data
            
            res = self.auth_login_with_form(username, password, remember)
            if res:
                return redirect(redirect_url)
        
        self.set_message('error', _('Login failed. Please try again!'), life=None)
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        language = self.get_locale()
        return LoginForm(self.request)


class LogoutHandler(AuthHandler):
    
    def get(self, **kwargs):
        self.auth_logout()
        return redirect(self.redirect_path())


class SignupHandler(AuthHandler):
    
    @login_required
    def get(self, **kwargs):
        if self.auth_current_user:
            return redirect(self.redirect_path())
        return self.render_response('user/signup.html', form=self.form)
    
    @login_required
    def post(self, **kwargs):
        redirect_url = self.redirect_path()
        
        if self.auth_current_user:
            return redirect(redirect_url)
        
        if self.form.validate():
            auth_id = self.auth_session.get('id')
            user = self.auth_create_user(self.form.nickname.data, auth_id)
            
            if user:
                self.auth_set_session(user.auth_id, user.session_id, '1')
                self.set_message('success', 'You are now registered', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This username is taken', life=None)
                return self.get(**kwargs)
        
        self.set_message('error', 'A problem occurred!', life=None)
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        return SignupForm(self.request)


class RegisterHandler(AuthHandler):
    
    def get(self, **kwargs):
        redirect_url = self.redirect_path()
        if self.auth_current_user:
            return redirect(redirect_url)
        return self.render_response('user/register.html', form=self.form)
    
    def post(self, **kwargs):
        redirect_url = self.redirect_path()
        if self.auth_current_user:
            return redirect(redirect_url)
        
        if self.form.validate():
            username = self.form.username.data
            password = self.form.password.data
            password_confirm = self.form.password_confirm.data
            email = self.form.email.data
            email_confirm = self.form.email_confirm.data
            
            if password != password_confirm:
                self.set_message('error', 'Password doesnt match', life=None)
                return self.get(**kwargs)
            
            if email != email_confirm:
                self.set_message('error', 'E-mail doesnt match', life=None)
                return self.get(**kwargs)
            
            auth_id = 'own|%s' % username
            user = self.auth_create_user(username, auth_id, password=password, email=email)
            if user:
                profile = Profile.create(user.key())
                if profile:
                    url = '/mail/verify/%s/' % user.key()
                    task = taskqueue.add(url=url, method='GET')
                self.auth_set_session(user.auth_id, user.session_id, '1')
                self.set_message('success', 'You are now registered', flash=True, life=5)
                return redirect(redirect_url)
            else:
                self.set_message('error', 'This username is taken', life=None)
                return self.get(**kwargs)
            
        self.set_message('error', 'A problem occurred!', life=None)
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        return RegistrationForm(self.request)


class FacebookHandler(AuthHandler, FacebookMixin):
    
    def head(self, **kwargs):
        return Response('')
    
    def get(self):
        url = self.redirect_path()
        if 'id' in self.auth_session:
            return redirect(url)
        
        self.session['_continue'] = url
        
        if self.request.args.get('session', None):
            return self.get_authenticated_user(self._on_auth)
        
        return self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            abort(403)
        
        username = user.pop('username', None)
        if not username:
            username = user.pop('uid', '')
        
        auth_id = 'facebook|%s' % username
        self.auth_login_with_third_party(auth_id, remember=True, session_key=user.get('session_key'))
        return self._on_auth_redirect()


class GoogleHandler(AuthHandler, GoogleMixin):
    def get(self):
        url = self.redirect_path()
        if 'id' in self.auth_session:
            return redirect(url)
        
        self.session['_continue'] = url
        
        if self.request.args.get('openid.mode', None):
            return self.get_authenticated_user(self._on_auth)
        
        return self.authenticate_redirect()
    
    def _on_auth(self, user):
        if not user:
            abort(403)
        
        auth_id = 'google|%s' % user.pop('email', '')
        self.auth_login_with_third_party(auth_id, remember=True)
        return self._on_auth_redirect()


class ProfileHandler(AuthHandler):
    
    @user_required
    def get(self, **kwargs):
        orders = Order.get_orders_by_user(self.auth_current_user)
        logging.info(orders)
        context = {
            'orders': orders,
        }
        # if not admin:
        # enable set/change:
        # email, password
        return self.render_response('user/profile.html', **context)


class VerifyProfileHandler(AuthHandler):
    
    def get(self, verification_code):
        verify = Profile.verify_code(verification_code)
        logging.info(verify)
        if verify == "verified" or "already_verified":
            return redirect_to('user/profile')
        else:
            return Response('Cannot verify you')
