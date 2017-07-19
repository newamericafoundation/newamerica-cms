import os
from createsend import *
from home.models import HomePage
from subscribe.models import SubscriptionSegment, SubscribePage

CREATESEND_API_KEY = os.getenv('CREATESEND_API_KEY')
CREATESEND_CLIENTID = os.getenv('CREATESEND_CLIENTID')
CREATESEND_LISTID = os.getenv('CREATESEND_LISTID')

def update_segments():
    cs = CreateSend({'api_key': CREATESEND_API_KEY})
    newamerica_list = List(cs.auth_details, CREATESEND_LISTID)

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
        if not exists:
            segment = SubscriptionSegment(title=cs_s.Title, SegmentID=cs_s.SegmentID, ListID=CREATESEND_LISTID)
            parent.add_child(instance=segment)
