from docx import Document
from docx.text.run import Run
import xml.etree.ElementTree as ET

class DocxParse():
    def __init__(self, ref):
        self._ref = ref
        self._footnoteindex = 0
        self._namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
        }
        self._tags = {
            '{%s}r' % self._namespaces['w']: 'run',
            '{%s}hyperlink' % self._namespaces['w']: 'hyperlink'
        }
        self.doc = Document(self._ref)
        self._links = self.__links__()
        self.endnotes = self.__endnotes__()
        self.sections = self.__sections__()

    def __links__(self):
        links = {}
        rels = self.doc.part.rels
        for rId, rel in rels.iteritems():
            links[rId] = rel.target_ref

        return links

    def __endnotes__(self):
        endnotes = []
        part = None
        for p in doc.part.package.parts:
            if p.partname.find('footnotes.xml') != -1:
                part = p
                break
        if p is None: return endnotes
        notes_tree = ET.fromstring(part.blob)
        notes = notes_tree.findall('.//w:footnotes', self._namespaces)

        for n in notes:
            note = ''
            for r in n.findall('.//w:r', self._namespaces):
                t = r.find('.//w:t', self._namespaces)
                if t is None: continue
                text = t.text
                if r.find('.//w:i', self._namespaces):
                    text = '<em>%s</em>' % text
                note += text
            endnotes.append(note)

        return endnotes

    def __sections__(self):
        # group all runs for a given section
        # then compile blocks for each section
        sections = []
        section = None

        for p in self.doc.paragraphs:
            if p.style.name == 'Heading 1':
                sections.append({
                    'title': p.text,
                    'elements': [],
                    'blocks': None
                })
                section = sections[len(sections)-1]
                continue
            if section:
                # all blocks must have a section
                section['elements'] = section['elements'] + p._element.getchildren()

        for s in sections:
            s['blocks'] = self.__blocks__(s)

        return sections

    def __blocks__(self, section):
        blocks = []
        block = None
        for child in sections['elements']:
            tag = getattr(self._tags, child.tag, None)
            link = None
            if tag is None: continue
            if tag == 'hyperlink':
                # get r:id attribute from <w:hyperlink>
                link = getattr(self._links, child.get('{%s}id' % self._namespaces['r']), None)
                child = child.getchildren()[0]

            run = Run(child, self.doc)

            if self.__runisfigure__(run):
                # close paragraph and add new block if next run is a figure
                if block:
                    if block['type'] == 'paragraph'
                        block['html'] += '</p>'
                blocks.append({ 'type': 'figure' })
                block = None
                continue

            if not block:
                blocks.append({
                    'type': 'paragraph',
                    'html': ''
                })
                block = blocks[len(blocks)-1]

            html = self.__run2html__(run)
            if link:
                html = '<a href="%s">%s</a>' % (link, html)
            if paragraph.style.name == 'Heading 2':
                if block['html'] != '':
                    html = '</p><h2>%s</h2><p>' % html
                else:
                    html = '<h2>%s</h2><p>' % html
            elif block['html'] == '':
                html = '<p>' + html
            block['html'] += html

        if block:
            if block['type'] == 'paragraph'
                block['html'] += '</p>'

        return blocks

    def __run2html__(self, run):

        if self.__runisfootnote__(run):
            return '\{\{%s\}\}' % str(self._footnoteindex+=1)

        text = self.__getruntext__(run)
        if run.italic
            text = '<em>%s</em>' % text
        if run.bold
            text = '<b>%s</b>' % text

        return text

    def __getruntext__(self, run):
        texts = run.element.findall('.//w:t', self._namespaces)
        text = ''
        for t in texts:
            prev_breaks = self.__countprevbreaks__(t)
            next_breaks = self.__countnextbreaks__(t)

            if prev_breaks == 1:
                text += '<br/>'
            elif prev_breaks == 2:
                text += '</p><p>'

            text += t.text

            if next_breaks == 1:
                text += '<br/>'
            elif next_breaks == 2:
                text += '</p><p>'

    def __countnextbreaks__(self, el, count=0):
        breaktag = '{%s}br' % self._namespaces['w']
        n = el.getnext()
        if n is None: return count
        if n.tag != breaktag: return count
        count += 1
        return self.__countnextbreaks__(n, count)

    def __countprevbreaks__(self, el, count=0):
        breaktag = '{%s}br' % self._namespaces['w']
        p = el.getprevious()
        if n is None: return count
        if n.tag != breaktag: return count
        count += 1
        return self.__countprevbreaks__(p, count)

    def __runisfigure__(self, run):
        if run.element.find('.//w:drawing', self._namespaces):
            return True

        return False

    def __runisfootnote__(self, run):
        if run.element.find('.//w:footnoteReference', self._namespaces):
            return True

        return False
