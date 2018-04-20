from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

from report.models import Report
from .tasks import write_pdf

def redirect_report_section(request, **kwargs):
    path = request.path.split('/')[:-2]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'report/report.html', context={ 'page': report })

def pdf(request, **kwargs):
    path = request.path.split('/')[:-2]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    if not report.report_pdf:
        return pdf_render(request, **kwargs)
    url = 'https://s3.amazonaws.com/newamericadotorg/' + report.report_pdf.file.name
    return redirect(url)

def pdf_render(request, **kwargs):
    path = request.path.split('/')[:-3]
    report = Report.objects.filter(slug=path[len(path)-1]).first()

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=%s.pdf' % report.title
    response['Content-Transfer-Encoding'] = 'binary'
    protocol = 'https://' if request.is_secure() else 'http://'
    base_url = protocol + request.get_host()

    html = loader.get_template('report/pdf.html').render({ 'page': report })
    pdf = write_pdf(response, html, base_url)

    return response

def pdf_html(request, **kwargs):
    path = request.path.split('/')[:-3]
    report = Report.objects.filter(slug=path[len(path)-1]).first()
    return render(request, 'report/pdf.html', context={ 'page': report })
