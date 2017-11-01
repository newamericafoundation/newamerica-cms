from django.shortcuts import render
from report.models import Report
from .pdf_gen import generate_pdf_response

def redirect_report_section(request, **kwargs):
    path = request.path.split('/')[:-2]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'report/report.html', context={ 'page': report })

def pdf(request, **kwargs):
    path = request.path.split('/')[:-2]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    return generate_pdf_response(report, request)
