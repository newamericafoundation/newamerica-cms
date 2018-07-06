from django.shortcuts import render, redirect

def future_property_rights(request, **kwargs):
    path = request.path.split('/')[3:]
    url = '/future-property-rights/' + '/'.join(path)
    return redirect(url)
