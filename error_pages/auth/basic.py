from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from error_pages.auth.base import BaseAuth


class BasicAuth(BaseAuth):
    '''Basic authentication decorator against django.contrib.auth
       user database.

       Decorate functions that need Basic authentication.

       Just subclass this class and re-implement any methods
       if you need to change the functionality.
    '''
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        username, password = self.get_credentials(args[0])

        res = self.login(args[0], username, password, *args, **kwargs)
        if res:
            return res

        return self.login_required(args[0])

    def login(self, request, username, password, *args, **kwargs):
        '''Login checking code

           Return and execute self.func (view function)
           if success, False or None otherwise.
        '''
        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                request.user = user
                login(request, user)
                return self.func(*args, **kwargs)

    def login_required(self, request):
        '''Return the correct response to initiate login'''
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        return response

    def get_credentials(self, request):
        '''Get the authentication credentials'''
        if self.auth_header in request.META:
            meth, auth = request.META[self.auth_header].split(' ', 1)
            if meth.lower() == 'basic':
                decoded = auth.decode('base64')
                return decoded.split(':', 1)

        return (None, None)


class BasicAuthError(Exception):
    '''Raise to invoke BasicAuth

       Just import this, and if you need, set callableObj
       to your custom subclassed BaseAuth.

    Args:
       view        : The function that gets evaluated if login
                     was successful
       *args, **kwargs : args and kwargs to pass to the view
    '''
    callableObj = BasicAuth

    def __init__(self, view, *args, **kwargs):
        self.view = view
        self.args = args
        self.kwargs = kwargs
