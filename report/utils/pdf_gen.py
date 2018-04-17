from weasyprint import HTML
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import tempfile

def generate_pdf_response(page, request=None):
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=%s.pdf' % page.title
    response['Content-Transfer-Encoding'] = 'binary'
    protocol = 'https://' if request.is_secure() else 'http://'
    base_url = protocol + request.get_host()
    
    html = loader.get_template('report/pdf.html').render({ 'page': page })
    pdf = HTML(string=html, base_url=base_url).write_pdf(response)

    return response
