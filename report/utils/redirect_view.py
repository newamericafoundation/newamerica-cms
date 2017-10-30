from django.shortcuts import render
from report.models import Report

def redirect_report(request, **kwargs):
    path = request.path.split('/')[:-2]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'report/report.html', context={ 'page': report })
