from .docx_parse import DocxParse
from newamericadotorg.blocks import PanelBlock
from report.blocks import EndnoteBlock, ReportBody, BoxBody
from wagtail.blocks.stream_block import StreamValue
from wagtail.rich_text import RichText
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock

def generate_docx_streamfields(document):
    parsed = DocxParse(document)
    panels = []
    figure_index = { 'i': 1 }
    box_num = 0
    for s in parsed.sections:
        if len(s.blocks) == 0:
            continue
        body = []
        for b in s.blocks:
            val = None
            if b['type'] == 'box':
                box_num += 1
                box_body = []
                for box_block in b['blocks']:
                    v = parse_block(box_block, figure_index)
                    if v:
                        box_body.append(v)
                title = 'Box %s' % box_num
                val = ('box', { 'title': title, 'body': StreamValue(BoxBody(), box_body) })
            else:
                val = parse_block(b, figure_index)

            if val is not None:
                body.append(val)

        panel = ('section', { 'title': s.title, 'body': StreamValue(ReportBody(), body) })
        panels.append(panel)

    endnotes = []
    for e in parsed.endnotes:
        endnotes.append(('endnote', { 'number': e['number'], 'note': RichText(e['note']) }))

    return { 'endnotes': endnotes, 'sections': panels }

def parse_block(b, figure_index):
    val = None
    if b['type'] == 'paragraph':
        val = ('paragraph', RichText(b['html']))
    elif b['type'] == 'heading':
        val = ('heading', b['text'])
    elif b['type'] == 'table':
        val = ('table', b['data'])
    elif b['type'] == 'inline_image':
        val = ('paragraph', RichText('<em>[[Figure %s]]</em>' % figure_index['i']))
        figure_index['i'] += 1

    return val
