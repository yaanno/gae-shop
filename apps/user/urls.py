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
            Rule('/sign-in/', endpoint='auth/login', handler='LoginHandler'),
            Rule('/sign-out/', endpoint='auth/logout', handler='LogoutHandler'),
            Rule('/sign-up/', endpoint='auth/signup', handler='SignupHandler'),
            Rule('/create-account/', endpoint='auth/register', handler='RegisterHandler'),
            Rule('/auth/facebook/', endpoint='auth/facebook', handler='FacebookHandler'),
            Rule('/auth/google/', endpoint='auth/google', handler='GoogleHandler'),
            Rule('/your/', endpoint='user/profile', handler='ProfileHandler'),
            Rule('/verify/<verification_code>/', endpoint='user/verify', handler='VerifyProfileHandler'),
        ]),
    ]
    
    return rules
