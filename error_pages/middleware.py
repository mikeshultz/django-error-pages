import logging

from django.template import Context, Template, loader
from django.core.exceptions import PermissionDenied
from django.conf.urls.defaults import include, patterns

from error_pages.template import process_template, process_messages
from error_pages import urls as urlconf
from error_pages.http import *

import settings


class ErrorPageMiddleware(object):

    def process_exception(self, request, exception):
        '''Process exceptions raised in view code'''
        template = code = None

        for i in globals():
            if i.startswith('Http'):
                if isinstance(exception, globals()[i]) or isinstance(exception, PermissionDenied):
                    code = int(i[-3:])
                    template = '%d.html' % code
                    break

        # handle special cases
        if code in [404, 500]:
            # let django handle these codes instead
            template = code = None

        if settings.DEBUG and code:
            # get the template page source
            TEMPLATE = process_template(code)

            # get the title
            title = process_messages(code)[0]
            # ok, now log a warning
            t = []
            for word in title.split(' '):
                t.append(word.capitalize())
            logging.warning('%s: %s' % (' '.join(t), request.path),
                            extra={
                                'status_code': code,
                                'request': request
                            })

        if template is not None:
            if settings.DEBUG:
                t = Template(TEMPLATE, name='Error Page Template')
            else:
                t = loader.get_template(template)

            return HttpResponse(t.render(Context({'request': request})), status=code)

    def process_request(self, request):
        '''Allow us to render error pages from external sources (such as Apache)'''
        original_urlconf = __import__(getattr(request, 'urlconf', settings.ROOT_URLCONF), {}, {}, ['*'])
        urlconf.urlpatterns += patterns('',
            ('', include(original_urlconf)),
        )

        if hasattr(original_urlconf, 'handler404'):
            urlconf.handler404 = original_urlconf.handler404
        if hasattr(original_urlconf, 'handler500'):
            urlconf.handler500 = original_urlconf.handler500

        request.urlconf = 'error_pages.urls'
