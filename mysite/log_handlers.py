import logging, traceback, os
from logdna import LogDNAHandler as LogDNA

class LogDNAHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            API_KEY = os.getenv('LOGDNA_KEY')
            handler = LogDNA(API_KEY,{
                'index_meta': True,
                'app': 'newamerica-cms',
                'level': 'Error',
                'hostname': os.getenv('HOSTNAME') or 'na-errors'
            })
            log = logging.getLogger('logdna')
            log.addHandler(handler)
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

                    log.error(error, {'context':context})

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
