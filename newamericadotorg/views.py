from django.shortcuts import render


def preview(request, **kwargs):
    return render(request, 'preview.html', context={})
