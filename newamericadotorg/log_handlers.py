import logging, traceback, os, sys, json
from newamericadotorg.helpers import is_json
from logdna import LogDNAHandler as LogDNA
from django.http import JsonResponse


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
        if 'api' in request.path:
            exc_info = sys.exc_info()

            exc_type, exc_val, exc_tb = exc_info
            tb = traceback.extract_tb(exc_tb)
            cause = tb[len(tb)-1]

            filename = cause[0]
            line = cause[1]
            msg = traceback.format_exception_only(exc_type, exc_val)[0].replace('\n','; ')

            error_source = 'file=%s line=%s' % (filename, line)
            logdna = LogDNAMiddleware(self.get_response)
            logdna.process_exception(request, exception)
            return JsonResponse({
                'count': None,
                'next': None,
                'previous': None,
                'results': [],
                'error': True,
                'error_source': error_source,
                'message': msg
            })

class LogDNAMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

        API_KEY = os.getenv('LOGDNA_KEY')
        handler = LogDNA(API_KEY,{
            'index_meta': True,
            'app': 'newamerica-cms',
            'level': 'Error',
            'hostname': os.getenv('HOSTNAME') or 'na-errors'
        })
        self.log = logging.getLogger('logdna')
        self.log.addHandler(handler)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        exc_info = sys.exc_info()

        exc_type, exc_val, exc_tb = exc_info
        tb = traceback.extract_tb(exc_tb)
        cause = tb[len(tb)-1]

        filename = cause[0]
        line = cause[1]
        msg = traceback.format_exception_only(exc_type, exc_val)[0].replace('\n','; ')

        error = 'file=%s line=%s msg="%s"' % (filename, line, msg)
        context = {
            'traceback': traceback.format_tb(exc_tb),
            'method': request.method,
            'path': request.path
        }

        for k,v in request.META.items():
            if isinstance(v, str):
                context[k] = v;

        self.log.error(error, {'context':context})
