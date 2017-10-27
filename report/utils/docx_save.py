from .docx_parse import DocxParse
from newamericadotorg.blocks import PanelBlock, Body
from report.blocks import EndnoteBlock
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.rich_text import RichText
from wagtail.wagtailcore import blocks

def generate_docx_streamfields(document):
    parsed = DocxParse(document)
    panels = []

    for s in parsed.sections:
        body = []
        for b in s['blocks']:
            if b['type'] == 'paragraph':
                val = ('paragraph', RichText(b['html']))
                body.append(val)
            # else:
            #     val = ('inline_image', {})
            # body.append(val)

        panel = ('section', { 'title': s['title'], 'body': StreamValue(Body(), body) })
        panels.append(panel)

    endnotes = []
    for e in parsed.endnotes:
        endnotes.append(('endnote', { 'number': e['number'], 'note': RichText(e['note']) }))

    return { 'endnotes': endnotes, 'sections': panels }
