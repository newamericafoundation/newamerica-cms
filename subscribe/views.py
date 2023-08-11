from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from wagtail.admin import messages
from wagtail.admin.auth import permission_required

from subscribe.campaign_monitor import update_segments


@permission_required("subscribe.can_sync_from_campaign_monitor")
def campaign_monitor_sync_view(request):
    if request.method == 'POST':
        created = update_segments()
        messages.success(request, f"Campaign Monitor sync complete: {created} segments created.")
        return redirect(reverse('wagtailadmin_home'))
    else:
        return TemplateResponse(request, 'wagtailadmin/campaign_monitor_sync.html')
