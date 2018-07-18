from time import gmtime, strftime

from weasyprint import HTML
from django.template import loader
import tempfile
from wagtail.documents.models import get_document_model
from newamericadotorg.celery import app as celery_app
from django.apps import apps
from wagtail.core.models import PageRevision
from .utils.docx_save import generate_docx_streamfields

@celery_app.task
def generate_pdf(report_id):
    Report = apps.get_model('report', 'Report')
    report = Report.objects.get(pk=report_id)
    contents = generate_report_contents(report)
    authors = get_report_authors(report)
    html = loader.get_template('report/pdf.html').render({ 'page': report, 'contents': contents, 'authors': authors })

    pdf = HTML(string=html).write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(pdf)
        output.flush()
        pdf = open(output.name, 'r')
        Document = get_document_model()
        doc = Document(title=report.title)
        last_edited = ' %s.pdf' % strftime('%Y-%m-%d %H:%M:%S', gmtime())
        doc.file.save(report.title + last_edited, pdf)
        report.report_pdf = doc
        report.generate_pdf_on_publish = False
        report.revising = False
        revision = report.save_revision()
        revision.publish()
        print('Generated PDF for %s' % report.title)

@celery_app.task
def write_pdf(response, html, base_url):
    return HTML(string=html, base_url=base_url).write_pdf(response)

@celery_app.task
def parse_pdf(page):
    page.overwrite_sections_on_save = False
    streamfields = generate_docx_streamfields(page.source_word_doc.file)
    page.sections = streamfields['sections']
    page.endnotes = streamfields['endnotes']


def generate_report_contents(report):
    contents = [[]]
    contents_count = 0;
    for s in report.sections:
        contents_count += 1
        if contents_count > 14:
            contents_count = 0;
            contents.append([])
        c = {
            'title': s.value['title'],
            'subsections': []
        }

        for sub in s.value['body']:
            if sub.block_type == 'heading':
                contents_count += 1
                c['subsections'].append(sub.value)

        contents[len(contents)-1].append(c)

    return contents


def get_report_authors(report):
    authors = None

    if report.authors:
        authors = report.authors.order_by('pk')

    return authors
