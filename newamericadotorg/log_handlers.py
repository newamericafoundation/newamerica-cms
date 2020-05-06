import logging, traceback, os, sys, json
from newamericadotorg.helpers import is_json
from logdna import LogDNAHandler as LogDNA
from django.http import JsonResponse
from django.conf import settings


class LoggerFilter(logging.Filter):
    def filter(self, record):
        print(record.getMessage())


logger = logging.getLogger('weasyprint')
logger.addFilter(LoggerFilter())


class APIExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if 'api' in request.path and not settings.DEBUG:
            exc_info = sys.exc_info()

            exc_type, exc_val, exc_tb = exc_info
            tb = traceback.extract_tb(exc_tb)
            cause = tb[len(tb)-1]

            filename = cause[0]
            line = cause[1]
            msg = traceback.format_exception_only(exc_type, exc_val)[0].replace('\n','; ')

            error_source = 'file=%s line=%s' % (filename, line)
            return JsonResponse({
                'count': None,
                'next': None,
                'previous': None,
                'results': [],
                'error': True,
                'error_source': error_source,
                'message': msg
            })

