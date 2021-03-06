Django Error Pages
==================

Django Error Pages extends Django to allow you to raise and handle any type of
HTTP error, such as 400, and 403.

It behaves just like the default Django 404 and 500 error pages, which render
404.html and 500.html respectively inside your apps template folder, but display
some information in DEBUG mode.

It will catch all Django error codes and return an error page.

It is very flexible, and covers a wide range of error codes:
400-418, 422-426,
500-505, 507, 509, 510

Configurability & Extendibility
-------------------------------

Django Error Pages is very easy to use!

How easy it is to raise a 403 forbidden:

```python
from django.shortcuts import render_to_response

from error_pages.http import Http403

def homepage(request):
    if user is unauthorized:
        raise Http403
    return render_to_response('index.html')
```

And of course, it'll render a 403.html template for you if DEBUG mode is off.

Also, I don't think Django handles some certain error pages, such as 400, 403,
(which shows some default error, but isn't overridable). So we now is included
the ability to render your Django template error pages directly from Apache!
It will render just as if Django was rendering a 404 page. Just place the
corresponding 400.html page into the template folder in your app, and add this
rule to your Apache configuration. You can do this with ANY error code you want,
just like you can raise any error code you want; why should anyone be restricted? :)

```apacheconf
ErrorDocument 400 /__errorpage__/400
```

Configuring & Setting up
------------------------

* Add it to your middleware

```python
MIDDLEWARE_CLASSES = (
    ...
    'error_pages.middleware.ErrorPageMiddleware',
)
```

* And add the URL configuration to your root URL's

```python
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    ...
    url(r'^__errorpage__/(?P<code>\d+)$', 'error_pages.views.display_error'),
)
```

Installing
----------

* Download django-error-pages from https://github.com/Roejames12/django-error-pages/tarball/master
* Or `pip install django-error-pages`
* `pip install django-error-pages==dev` for the absolute bleeding edge.
