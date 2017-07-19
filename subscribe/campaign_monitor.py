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

    cs_segments = newamerica_list.segments()
    existing_segments = SubscriptionSegment.objects.all()

    parent = SubscribePage.objects.first()
    if not parent:
        home = HomePage.objects.first()
        parent = home.add_child(instance=SubscribePage(title='New America Subscription Lists'))

    for cs_s in cs_segments:
        exists = False
        for s in existing_segments:
            if s.SegmentID == cs_s.SegmentID:
                exists = True
                s.title = cs_s.title
                s.update()

        if not exists:
            segment = SubscriptionSegment(title=cs_s.Title, SegmentID=cs_s.SegmentID, ListID=CREATESEND_LISTID)
            parent.add_child(instance=segment)

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
    except BadRequest:
        subscriber.add(CREATESEND_LISTID, email, name, custom_fields, True)
