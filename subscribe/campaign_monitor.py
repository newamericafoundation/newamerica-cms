import logging, traceback, os, sys
from django.conf import settings
from createsend import *
from home.models import HomePage
from subscribe.models import SubscriptionSegment, SubscribePage
from logdna import LogDNAHandler as LogDNA

LOGDNA_KEY = os.getenv('LOGDNA_KEY')
CREATESEND_API_KEY = os.getenv('CREATESEND_API_KEY')
CREATESEND_CLIENTID = os.getenv('CREATESEND_CLIENTID')
CREATESEND_LISTID = os.getenv('CREATESEND_LISTID')
auth = {'api_key': CREATESEND_API_KEY}

def update_segments():
    newamerica_list = List(auth, CREATESEND_LISTID)

    fields = newamerica_list.custom_fields()
    segments = None
    for f in fields:
        if f.FieldName=='Subscriptions':
            segments=f.FieldOptions

    existing_segments = SubscriptionSegment.objects.all()

    parent = SubscribePage.objects.first()
    if not parent:
        home = HomePage.objects.first()
        parent = home.add_child(instance=SubscribePage(title='New America Subscription Lists'))

    for segment in segments:
        exists = False
        for e_segment in existing_segments:
            if e_segment.title == segment:
                exists = True

        if not exists:
            seg = SubscriptionSegment(title=segment, SegmentID=segment, ListID=CREATESEND_LISTID)
            parent.add_child(instance=seg)

def update_subscriber(email, name, custom_fields):
    subscriber = Subscriber(auth, CREATESEND_LISTID, email)
    try:
        s = subscriber.get()
        # prevent overwriting Subscriptions by merging existing data
        for cf in s.CustomFields:
            exists = False
            for new_cf in custom_fields:
                if cf.Key == 'Subscriptions' and cf.Value == new_cf['value']:
                    exists = True
            if not exists:
                custom_fields.append({ 'key': cf.Key, 'value': cf.Value })

        subscriber.update(email, name, custom_fields, True, "Unchanged")
        return 'OK'
    except BadRequest:
        try:
            subscriber.add(CREATESEND_LISTID, email, name, custom_fields, True, "Unchanged")
            return 'OK'
        except:
            if not settings.DEBUG:
                handler = LogDNA(LOGDNA_KEY,{
                    'index_meta': True,
                    'app': 'newamerica-cms',
                    'level': 'Error',
                    'hostname': os.getenv('HOSTNAME') or 'na-errors'
                })
                log = logging.getLogger('logdna')
                log.addHandler(handler)
                error = get_error(sys.exc_info())
                log.error(error['msg'], {'context': error['context']})
            return 'BAD_REQUEST'

def get_error(exc_info):
    exc_type, exc_val, exc_tb = exc_info
    tb = traceback.extract_tb(exc_tb)
    cause = tb[len(tb)-1]

    filename = cause[0]
    line = cause[1]
    msg = traceback.format_exception_only(exc_type, exc_val)[0].replace('\n','; ')

    error = 'file=%s line=%s msg="%s"' % (filename, line, msg)
    context = {
        'traceback': traceback.format_tb(exc_tb)
    }

    return {
        'msg': error,
        'context': context
    }
