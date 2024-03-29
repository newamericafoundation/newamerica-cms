import traceback

import createsend
from django.conf import settings

from subscribe.models import MailingListSegment

auth = {"api_key": settings.CREATESEND_API_KEY}


def update_segments():
    newamerica_list = createsend.List(auth, settings.CREATESEND_LISTID)

    fields = newamerica_list.custom_fields()
    segments = None
    for f in fields:
        if f.FieldName == "Subscriptions":
            segments = set(f.FieldOptions)

    existing_segments = set(
        MailingListSegment.objects.values_list("title", flat=True)
    )
    created = 0
    for segment in segments.difference(existing_segments):
        MailingListSegment.objects.create(title=segment)
        created += 1
    return created


def update_subscriber(email, name, custom_fields):
    subscriber = createsend.Subscriber(auth, settings.CREATESEND_LISTID, email)
    try:
        s = subscriber.get()
        # prevent overwriting Subscriptions by merging existing data
        for cf in s.CustomFields:
            exists = False
            for new_cf in custom_fields:
                if cf.Key == "Subscriptions" and cf.Value == new_cf["value"]:
                    exists = True
            if not exists:
                custom_fields.append({"key": cf.Key, "value": cf.Value})

        subscriber.update(email, name, custom_fields, True, "Unchanged")
    except createsend.BadRequest:
        try:
            subscriber.add(
                settings.CREATESEND_LISTID,
                email,
                name,
                custom_fields,
                True,
                "Unchanged",
            )
        except Exception:
            return "BAD_REQUEST"

    return "OK"


def get_error(exc_info):
    exc_type, exc_val, exc_tb = exc_info
    tb = traceback.extract_tb(exc_tb)
    cause = tb[len(tb) - 1]

    filename = cause[0]
    line = cause[1]
    msg = traceback.format_exception_only(exc_type, exc_val)[0].replace(
        "\n", "; "
    )

    error = 'file=%s line=%s msg="%s"' % (filename, line, msg)
    context = {"traceback": traceback.format_tb(exc_tb)}

    return {"msg": error, "context": context}
