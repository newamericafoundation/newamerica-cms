from weasyprint import HTML
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
import tempfile

def generate_pdf_response(page, request=None):

    html = loader.get_template('report/pdf.html').render({ 'page': page })
    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=%s.pdf' % page.title 
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())
    #return render(request, 'report/pdf.html', context={ 'page': page })
    return response
