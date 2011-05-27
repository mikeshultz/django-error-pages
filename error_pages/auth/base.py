class BaseAuth(object):
    # the realm from which the site message appears on the login box
    realm = ''
    # name of request header to grab username from
    user_header = 'REMOTE_USER'
    # name of the header to grab the auth details from
    auth_header = 'HTTP_AUTHORIZATION'

    # fix problem with django-debug-toolbar
    __name__ = 'BaseAuth'
