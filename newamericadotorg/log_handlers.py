import logging


class LoggerFilter(logging.Filter):
    def filter(self, record):
        print(record.getMessage())


logger = logging.getLogger('weasyprint')
    .addFilter(LoggerFilter())
