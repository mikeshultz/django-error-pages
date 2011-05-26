Configuring
===========

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

Settings
--------

### ERRORPAGES_PAGES_ENABLED

This setting allows you to disable all error pages (DEBUG error pages, and
the error pages in your template; 400.html, 401.html, etc.)

Default: True

### ERRORPAGES_PAGES_IGNORE

This setting allows you to ignore specific error pages.

Default: 405, 410
