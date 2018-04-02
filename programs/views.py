from django.shortcuts import render

from programs.models import Program, Subprogram, Project
from django.http import HttpResponseRedirect
from wagtail.wagtailcore import views

def redirect_to_program(request, **kwargs):
    program = Program.objects.filter(slug=kwargs['program']).first()
    return render(request, 'programs/program.html', context={ 'page': program })

def redirect_to_subprogram(request, **kwargs):
    program = Subprogram.objects.filter(slug=kwargs['subprogram']).first()
    return render(request, 'programs/program.html', context={ 'page': program })

def redirect_project_page(request, **kwargs):
    program = Subprogram.objects.filter(slug=kwargs['subprogram']).first()
    if not program:
        return views.serve(request, request.path)

    program = program.specific
    redirect_page = getattr(program, 'redirect_page', None)
    if redirect_page:
        return HttpResponseRedirect(redirect_page.url)
    else:
        return render(request, 'programs/program.html', context={ 'page': program })
