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
