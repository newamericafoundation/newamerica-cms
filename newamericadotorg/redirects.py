from django.shortcuts import render, redirect


# Subprograms changing to programs

def future_property_rights(request, **kwargs):
    path = request.path.split('/')[3:]
    url = '/future-property-rights/' + '/'.join(path)
    return redirect(url)

def new_practice_lab(request, **kwargs):
    path = request.path.split('/')[3:]
    url = '/new-practice-lab/' + '/'.join(path)
    return redirect(url)


# Name changes

def dual_language_learners(request, **kwargs):
    path = request.path.split('/')
    path[2] = 'english-learners'
    url = '/'.join(path)
    return redirect(url)

def digi(request, **kwargs):
    path = request.path.split('/')
    path[1] = 'digital-impact-governance-initiative'
    url = '/'.join(path)
    return redirect(url)

def local(request, **kwargs):
    path = request.path.split('/')
    path[1] = 'local'
    url = '/'.join(path)
    return redirect(url)
