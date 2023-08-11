from django.http import HttpResponse
from wagtail.admin.auth import permission_required

from subscribe.campaign_monitor import update_segments


@permission_required("subscribe.can_sync_from_campaign_monitor")
def campaign_monitor_sync_view(request):
    update_segments()
    return HttpResponse("Campaign monitor sync complete")
