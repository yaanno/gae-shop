# -*- coding: utf-8 -*-
"""
    User model
"""
import logging

from tipfy.ext.auth.model import User, gen_salt
import tipfy.ext.i18n as i18n

from google.appengine.ext import db


class Profile(db.Model):
    verified = db.BooleanProperty(default=False)
    verification_code = db.StringProperty(default="")
    first_name = db.StringProperty(default="")
    last_name = db.StringProperty(default="")
    user = db.ReferenceProperty(User)
    language = db.StringProperty(default="hu_HU")
    
    @classmethod
    def create(self, user=None):
        
        def txn():
            code = gen_salt(20)
            language = i18n.get_locale()
            profile = Profile(user=user, verification_code=code, language=language)
            profile.put()
            return profile
        
        return db.run_in_transaction(txn)
    
    @classmethod
    def verify_code(self, verification_code=None):
        
        query = self.all()
        query.filter("verification_code =", verification_code).filter("verified =", False)
        profile = query.get()
        if profile:
            return self.set_verified(profile)
        else:
            return "already_verified"
    
    @classmethod
    def set_verified(self, profile=None):
        
        def txn():
            _profile = Profile.get(profile.key())
            _profile.verified = True
            if _profile.put():
                return "verified"
            return "couldnt_verify"
        
        return db.run_in_transaction(txn)


