from docx import Document
from docx.text.run import Run
from docx.table import Table
import xml.etree.ElementTree as ET

from .block_utils import *
from .settings import NAMESPACES

def parse_paragraph(run, paragraph):
    style_name = paragraph.style.name

    text = parse_run_text(run)
    if run.italic:
        text = '<em>%s</em>' % text
    if run.bold:
        text = '<b>%s</b>' % text
    if style_name == 'Heading 3':
        text = '<h3>%s</h3>' % text
    if style_name == 'Heading 4':
        text = '<h4>%s</h4>' % text
    if style_name == 'Heading 5':
        text = '<h5>%s</h5>' % text

    return text

def parse_table(table, section):
    data = []

    for row in table.rows:
        r = []
        for cell in row.cells:
            text = ''
            for p in cell.paragraphs:

                p_text = ''
                for child in p._element.getchildren():
                    tag = TAGS.get(child.tag, None)
                    linkId = None
                    if tag == 'break' or tag == None:
                        continue
                    elif tag == 'hyperlink':
                        linkId = childishyperlink(child)
                        child = child.find('.//w:r', NAMESPACES)

                    run = Run(child, p)
                    footnote = runisfootnote(run)

                    if footnote:
                        p_text += '{{%s}}' % footnote
                    elif tag == 'hyperlink':
                        # markdown link
                        p_text += '[%s](%s)' % (run.text, section._links.get(linkId, None))
                    else:
                        p_text += run.text

                text += p_text

            r.append(text)
        data.append(r)

    return {
        'data': data,
        'first_row_is_table_header': True
    }

def convert_table_child(child, doc):
    if child.tag == '{%s}tbl' % NAMESPACES['w']:
        tbl = Table(child, doc._body)
        return tbl

    return False

def parse_run_text(run):
    texts = run.element.findall('.//w:t', NAMESPACES)
    text = ''
    for t in texts:
        text += t.text

    return text

def parse_links(rels):
    links = {}
    for rId, rel in rels.items():
        links[rId] = rel.target_ref

    return links

def parse_endnotes(parts):
    endnotes = []
    part = None
    for p in parts:
        if p.partname.find('footnotes.xml') != -1:
            part = p
            break
    if part is None: return endnotes
    notes_tree = ET.fromstring(part.blob)
    notes = notes_tree.findall('.//w:footnote', NAMESPACES)

    note_index = 0;
    for i, n in enumerate(notes):
        note = ''
        for r in n.findall('.//w:r', NAMESPACES):
            t = r.find('.//w:t', NAMESPACES)
            if t is None: continue
            text = t.text
            if r.find('.//w:i', NAMESPACES) is not None:
                text = '<em>%s</em>' % text
            note += text

        if note=='':
            continue
        note_index += 1
        endnotes.append({ 'number': note_index, 'note': note.strip() })

    return endnotes

def parse_list(el, section):
    listtype = el._elements[0][2][0]
    list = ''
    items = ''
    item = ''
    for i, e in enumerate(el._elements):
        child, paragraph, attrs = e
        type_, lvl = attrs

        tag = TAGS.get(child.tag, None)
        linkId = None
        if tag == 'break' or tag == None:
            continue
        elif tag == 'hyperlink':
            linkId = childishyperlink(child)
            child = child.find('.//w:r', NAMESPACES)

        run = Run(child, paragraph)
        p = parse_paragraph(run, paragraph)
        if tag == 'hyperlink':
            p = '<a href="%s">%s</a>' % (section._links.get(linkId, None), p)

        item += p

        add = False
        nest = False
        if i == len(el._elements)-1:
            add = True
            if lvl == '1':
                nest = True
        elif el._elements[i+1][1] != paragraph:
            add = True
            if lvl == '1' and el._elements[i+1][2][1] == '0':
                nest = True

        if add:
            item = '<li>%s</li>' % item
            items += item
            item = ''
        if nest:
            items = u"<{0}>{1}</{0}>".format(type_, items)
            list += items
            items = ''
        elif add and lvl == '0':
            list += items
            items = ''

    return u"<{0}>{1}</{0}>".format(listtype, list)


def parse_hyperlink(el, section):
    html_ = ''
    url = ''
    for e in el._elements:
        child, paragraph, linkId = e
        url = section._links.get(linkId, None)
        run = Run(child, paragraph)
        html_ += parse_paragraph(run, paragraph)

    return '<a href="%s">%s</a>' % (url, html_)

def parse_break(el, html):
    return ''
    # skip first and last breaks
    if html[-2:] == 'p>': return ''
    if len(el._elements) == 1:
        #return '</p><p>'
        return '<br/>'
    else:
        return '</p><p>'

def parse_footnote(el):
    child, paragraph, n = el._elements[0]

    return '{{%s}}' % n
