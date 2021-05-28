from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def preview(request, **kwargs):
    return render(request, 'preview.html', context={})
