from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key
import hashlib
from django.utils.encoding import force_bytes, force_text, iri_to_uri
import socket

def expire_page_cache(view_name, args=None):
    try:
        if args is None:
            path = reverse(view_name)
        else:
            path = reverse(view_name, args=args)

        request = HttpRequest()
        request.path = path
        request.META['SERVER_NAME'] = socket.gethostname()
        request.META['SERVER_PORT'] = 80
        url = request.build_absolute_uri()
        key = hashlib.md5(force_bytes(iri_to_uri(url))).hexdigest()

        caches = cache.keys('*%s*' % key)
        for key in caches:
            if cache.has_key(key):
                cache.delete(key)
        print('EXPIRED_CACHE: ' + url)
    except:
        print('FAILED_EXPIRED_CACHE: ' + view_name)
