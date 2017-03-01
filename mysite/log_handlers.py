import logging, traceback, os
from logdna import LogDNAHandler as LogDNA

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

    def process_exception(request, exception):
        print exception
        try:
            if record:
                if record.exc_info is not None:
                    exc_type, exc_val, exc_tb = record.exc_info
                    tb = traceback.extract_tb(exc_tb)
                    cause = tb[len(tb)-1]

                    filename = cause[0]
                    line = cause[1]
                    msg = traceback.format_exception_only(exc_type, exc_val)[0].replace('\n','; ')

                    error = 'file=%s line=%s msg="%s"' % (filename, line, msg)
                    context = {
                        'traceback': traceback.format_tb(exc_tb)
                    }

                    self.log.error(error, {'context':context})

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
