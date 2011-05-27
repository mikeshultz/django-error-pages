How to use it
=============

Raising HTTP codes
------------------

This is a quite simple and trivial task.

```python
from error_pages.http import Http400

def some_view(request):
    if some_condition:
        raise Http400

    return render_to_response('tmpl.html')
```

In the case of HTTP code 401 (user authorization),
simply raising it isn't going to pull up a login dialog
for the user. So we've made a way to do this.

Note: Handling the login after the user has entered something is beyond
the scope of this app and tutorial, however WSGI > 2.0, and mod_python
have the ability to handle these, and also Django. Just do a little
searching and you'll quickly find out what to do.

In order to do Basic Authentication, just use BasicAuth.
By default, it authenticates against the django auth user db,
but you can subclass BasicAuth and change code if you need to.
A 401.html template will be provided on authentication
failure as usual.

```python
from error_pages.auth import BasicAuth

class ViewOrBasicAuth(BasicAuth):
    realm = 'MyRealm'

@ViewOrBasicAuth
def homepage(request):
    return render_to_response('index.html')
```

After you handle a login, the ErrorPageMiddleware will check if any user
is logged in, and if so, it'll skip the error page and return a regular response.
However, you may want to custom handle this part; perhaps you have an extensive
permission system, then the code there will simply not suffice. We haven't forgotten
about you! Just do this.. Make sure your function either returns None or the response
if success.

```python
from error_pages import middleware

def handle_login_checking(self, request, response):
    if user_has_permission:
        return response

handle_authenticated_user = handle_login_checking
```

When in DEBUG mode, a default DEBUG template will be shown displaying
the error code, message, what the error means. When DEBUG mode is off,
a .html template file will be searched for. For example, if you're raising
HTTP 400, a file 400.html will be looked for in your apps template directory.

Integrating with your webserver
-------------------------------

So now you wonder, what about when my webserver pops up an error? Won't it go
to the standard default error page? Well, I don't know the internals of WSGI;
it may very well be that all the HTTP status errors are forwarded to the Python
app to be handled inside it. However, if never need be, you do have a way to point
server error documents to Django.

Make sure you first added the URL rules in docs/install.

Just point all your error documents to the URL like so. For Apache:

```apacheconf
ErrorDocument 400 /__errorpage__/400
```

Then Django will look for 400.html in your apps directory, and render it.
