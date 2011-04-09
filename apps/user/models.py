# -*- coding: utf-8 -*-
"""
    User model
"""
import logging

from tipfy.ext.auth.model import User, gen_salt
from google.appengine.ext import db


class Profile(db.Model):
    verified = db.BooleanProperty(default=False)
    verification_code = db.StringProperty(default="")
    first_name = db.StringProperty(default="")
    last_name = db.StringProperty(default="")
    user = db.ReferenceProperty(User)
    
    @classmethod
    def create(self, user=None):
        
        def txn():
            code = gen_salt(20)
            profile = Profile(user=user, verification_code=code)
            profile.put()
            return profile
        
        return db.run_in_transaction(txn)
    
    @classmethod
    def verify_code(self, verification_code=None):
        
        query = self.all()
        query.filter("verification_code =", verification_code).filter("verified =", False)
        profile = query.get()
        if profile:
            self.set_verified(profile)
        else:
            return True
    
    @classmethod
    def set_verified(self, profile=None):
        
        def txn():
            _profile = Profile.get(profile.key())
            _profile.verified = True
            if _profile.put():
                return True
            return False
        
        return db.run_in_transaction(txn)


