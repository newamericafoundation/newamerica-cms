from django.http import HttpResponse

from subscribe.campaign_monitor import update_segments


def campaign_monitor_sync_view(request):
    update_segments()
    return HttpResponse("Campaign monitor sync complete")
