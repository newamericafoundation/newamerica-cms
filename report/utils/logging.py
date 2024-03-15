import json


class StructuredMessage:
    def __init__(self, message, /, **kwargs):
        self.message = message
        self.kwargs = kwargs

    def __str__(self):
        return '%s %s' % (self.message, json.dumps(self.kwargs))
