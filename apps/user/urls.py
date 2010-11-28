# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

"""
from tipfy import Rule, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the Users application.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.user.handlers.', [
            Rule('/login/', endpoint='auth/login', handler='LoginHandler'),
            Rule('/logout/', endpoint='auth/logout', handler='LogoutHandler'),
            Rule('/signup/', endpoint='auth/signup', handler='SignupHandler'),
            Rule('/register/', endpoint='auth/register', handler='RegisterHandler'),
            
            Rule('/auth/facebook/', endpoint='auth/facebook', handler='FacebookHandler'),
            Rule('/auth/google/', endpoint='auth/google', handler='GoogleHandler'),
            
            Rule('/your/', endpoint='user/profile', handler='ProfileHandler'),
        ]),
    ]
    
    return rules
