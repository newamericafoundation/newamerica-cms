from time import gmtime, strftime
from io import BytesIO

from weasyprint import HTML
from django.template import loader
import tempfile
from wagtail.documents import get_document_model
from newamericadotorg.celery import app as celery_app
from django.apps import apps
from .utils.docx_save import generate_docx_streamfields
from .utils.pdf_service import render_pdf
from django.utils.text import slugify


@celery_app.task
def generate_pdf(report_id):
    # Generate report HTML
    Report = apps.get_model('report', 'Report')
    report = Report.objects.get(pk=report_id)
    revision = report.get_latest_revision_as_object()
    contents = generate_report_contents(revision)
    authors = get_report_authors(revision)
    html = loader.get_template('report/pdf.html').render({ 'page': revision, 'contents': contents, 'authors': authors, 'report': report })

    # Create a Document with empty file on S3 to hold the PDF
    Document = get_document_model()
    doc = Document(title=report.title)
    last_edited = ' %s.pdf' % strftime('%Y-%m-%d %H:%M:%S', gmtime())
    doc.file.save(revision.title + last_edited, BytesIO())

    # Submit request to PDF generator
    upload_successful = render_pdf(html, doc.file.name)

    if upload_successful:
        revision.report_pdf = doc
        revision.generate_pdf_on_publish = False
        revision.save_revision()


def write_pdf(response, html, base_url):
    return HTML(string=html, base_url=base_url).write_pdf(response)

@celery_app.task
def parse_pdf(page):
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
            'slug': slugify(s.value['title']),
            'subsections': []
        }

        for sub in s.value['body']:
            if sub.block_type == 'heading':
                contents_count += 1
                sub_s = {
                    'title': sub.value,
                    'slug': slugify(sub.value)
                }
                c['subsections'].append(sub_s)

        contents[len(contents)-1].append(c)

    return contents


def get_report_authors(report):
    authors = None

    if report.authors:
        authors = report.authors.order_by('pk')

    return authors
