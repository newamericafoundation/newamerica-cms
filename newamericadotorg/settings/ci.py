import os

from .base import *

BASE_URL = "http://testserver"

SECRET_KEY = "TEST_KEY"

WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'search.backend',
        'URLS': [os.getenv('ELASTIC_SEARCH_URL')],
        'INDEX': 'test',
        'TIMEOUT': 1500,
        'INDEX_SETTINGS': {
            'settings': {
                'index': {
                    'number_of_shards': 1,
                },
            },
        }
    }
}

TEST_ELASTICSEARCH = True
