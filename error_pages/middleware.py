import logging

from django.template import Context, Template, loader
from django.core.exceptions import PermissionDenied

from error_pages.template import process_template, process_messages
from error_pages.http import *

import settings


class ErrorPageMiddleware(object):

    def process_exception(self, request, exception):
        '''Process exceptions raised in view code'''
        template = code = None

        for i in globals():
            if i.startswith('Http'):
                http_match = isinstance(exception, globals()[i])
                perm_deny = isinstance(exception, PermissionDenied)
                if http_match or perm_deny:
                    if http_match:
                        code = int(i[-3:])
                    elif perm_deny:
                        code = 403

                    template = '%d.html' % code
                    break

        # handle special cases
        if code in [404, 500]:
            # let django handle these codes instead
            template = code = None

        if settings.DEBUG and code:
            # get the template page source
            TEMPLATE = process_template(code)

            # ok, now log a warning
            title = process_messages(code)[0]
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
