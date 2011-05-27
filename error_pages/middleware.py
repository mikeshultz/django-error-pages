import logging

from django.template import Context, Template, loader
from django.core.exceptions import PermissionDenied

from error_pages.auth import BasicAuthError
from error_pages.template import process_template, process_messages
from error_pages import config
from error_pages.http import *


# set this to a function for custom handling
# of the login checking part of ErrorPageMiddleware
handle_authenticated_user = None


class ErrorPageMiddleware(object):
    def __init__(self):
        self.template = self.code = None

    def process_exception(self, request, exception):
        '''Process exceptions raised in view code'''
        for i in globals():
            perm_deny = isinstance(exception, PermissionDenied)
            basic_error = isinstance(exception, BasicAuthError) or issubclass(exception, BasicAuth)
            if perm_deny or basic_error:
                if perm_deny:
                    self.code = 403
                    self.template = '%d.html' % self.code
                    break
                elif basic_error:
                    if not request.user.is_authenticated():
                        return exception.callableObj(exception.view).__call__(request, *exception.args, **exception.kwargs)

            if i.startswith('Http'):
                http_match = isinstance(exception, globals()[i])
                if http_match:
                    self.code = int(i[-3:])
                    self.template = '%d.html' % self.code
                    break

    def process_response(self, request, response):
        '''Process the response by status code'''

        # no exception raised by user, but it could still be error page worthy
        if not self.code:
            if response.status_code in [400, 401, 402, 403, 404, 405, 406, 407, 408,
                                        409, 410, 411, 412, 413, 414, 415, 416, 417,
                                        418, 422, 423, 424, 425, 426,
                                        500, 501, 502, 503, 504, 505, 507, 509, 510]:
                self.code = response.status_code
                self.template = '%d.html' % response.status_code

        # handle some special cases
        if self.code in [404, 500]:
            # let django handle these codes instead
            self.template = self.code = None
        elif self.code == 401:
            # return normal response for logged in users
            if not handle_authenticated_user:
                if request.user.is_authenticated():
                    return response
            else:
                # provide your own login checking code here
                res = handle_authenticated_user(self, request, response)
                if res:
                    return res

        # ok, now log a warning
        if config.DEBUG and self.code:
            title = process_messages(self.code)[0]
            t = []
            for word in title.split(' '):
                t.append(word.capitalize())
            logging.warning('%s: %s' % (' '.join(t), request.path),
                            extra={
                                'status_code': self.code,
                                'request': request
                            })

        if self.template is not None:
            # dont alter the response if we don't want the error page rendered
            if config.ERRORPAGES_PAGES_ENABLED and self.code not in config.ERRORPAGES_PAGES_IGNORE:
                if config.DEBUG:
                    TEMPLATE = process_template(self.code)
                    t = Template(TEMPLATE, name='Error Page Template')
                else:
                    t = loader.get_template(self.template)

                headers = response.__dict__['_headers']
                response = HttpResponse(t.render(Context({'request': request})), status=self.code)
                response.__dict__['_headers'].update(headers)

        return response
