import os
from createsend import *
from home.models import HomePage
from subscribe.models import SubscriptionSegment, SubscribePage

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

        subscriber.update(email, name, custom_fields, True)
        return 'OK'
    except BadRequest:
        subscriber.add(CREATESEND_LISTID, email, name, custom_fields, True)
        return 'BAD_REQUEST'
