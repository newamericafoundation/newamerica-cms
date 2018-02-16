from django.shortcuts import render

from programs.models import Program, Subprogram

def redirect_to_program(request, **kwargs):
    path = request.path.split('/')[:-2]
    program = Program.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'programs/program.html', context={ 'page': program })

def redirect_to_subprogram(request, **kwargs):
    path = request.path.split('/')[:-2]
    program = Subprogram.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'programs/program.html', context={ 'page': program })
