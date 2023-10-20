from django.contrib.auth.decorators import user_passes_test
from django.core.cache import cache
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from wagtail.admin import messages


@user_passes_test(lambda user: user.is_superuser)
def clear_cache_view(request):
    if request.method == "POST":
        cache.clear()
        messages.success(request, "Cache cleared")
        return redirect(reverse("wagtailadmin_home"))
    else:
        return TemplateResponse(request, "wagtailadmin/clear_cache.html")
