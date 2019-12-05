from django.shortcuts import render, redirect

def future_property_rights(request, **kwargs):
    path = request.path.split('/')[3:]
    url = '/future-property-rights/' + '/'.join(path)
    return redirect(url)

def dual_language_learners(request, **kwargs):
    path = request.path.split('/')
    path[2] = 'english-learners'
    url = '/'.join(path)
    return redirect(url)

def digi(request, **kwargs):
    path = request.path.split('/')
    path[1] = 'digital-impact-governance-inititiative'
    url = '/'.join(path)
    return redirect(url)
