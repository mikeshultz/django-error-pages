from django.http import HttpResponse

class BasicAuth(object):
    '''Basic authentication decorator

       Decorate functions that need Basic authentication.

       Just subclass this class and implement the authenticate
       method. Return True on success, None or False on failure.
    '''
    def __init__(self, realm):
        self.realm = realm

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            if self.authenticate(args[0]):
                return func(*args, **kwargs)
            else:
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
                return response

        return wrapped

    def authenticate(self, request):
        raise NotImplementedError
