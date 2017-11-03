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
        for p in self.doc.part.package.parts:
            if p.partname.find('footnotes.xml') != -1:
                part = p
                break
        if part is None: return endnotes
        notes_tree = ET.fromstring(part.blob)
        notes = notes_tree.findall('.//w:footnote', self._namespaces)

        for i, n in enumerate(notes):
            note = ''
            for r in n.findall('.//w:r', self._namespaces):
                t = r.find('.//w:t', self._namespaces)
                if t is None: continue
                text = t.text
                if r.find('.//w:i', self._namespaces) is not None:
                    text = '<em>%s</em>' % text
                note += text
            endnotes.append({ 'number': i+1, 'note': note.strip() })

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
            # all blocks must have a section
            if section:
                elements = []
                # python-docx ignores w:hyperlink tags...
                # create tuple of all elements + parent paragraph
                # and reinstantiate Run in loop
                for c in p._element.getchildren():
                    elements.append((c,p))
                section['elements'] = section['elements'] + elements

        for s in sections:
            s['blocks'] = self.__blocks__(s)
            del s['elements']

        return sections

    def __blocks__(self, section):
        blocks = []
        block = None
        prev_paragraph = None # track when there is a new w:p in order to reset html
        r_index = 0 # track run index within a w:p. resets to 0 with new w:p or after a heading or figure
        this_list = None
        prev_list = None
        for child, paragraph in section['elements']:
            # only parsing tags specified in self._tags
            tag = self._tags.get(child.tag, None)
            link = None
            if tag is None: continue
            if tag == 'hyperlink':
                rId = child.get('{%s}id' % self._namespaces['r'])
                link = self._links.get(rId, None)
                child = child.getchildren()[0]
                if child is None: continue

            run = Run(child, paragraph)

            if self.__runisfigure__(run):
                self.__closeblock__(block, prev_list)
                blocks.append({ 'type': 'inline_image' })
                block = None
                r_index = 0
                this_list = None
                continue

            if run.text == '' and not self.__runisfootnote__(run):
                continue

            if paragraph.style.name == 'Heading 2':
                self.__closeblock__(block, prev_list)
                blocks.append({ 'type': 'heading', 'text': run.text })
                block = None
                r_index = 0
                this_list = None
                continue

            if block is None:
                blocks.append({
                    'type': 'paragraph',
                    'html': ''
                })
                block = blocks[len(blocks)-1]

            if prev_paragraph != paragraph:
                r_index = 0
                this_list = self.__getparagraphlist__(paragraph)
                prev_list = self.__getparagraphlist__(prev_paragraph)
                # if it's a list
                if this_list is not None:
                    if prev_list is None:
                        l = '<ul>' if this_list == 'unordered' else '<ol>'
                        block['html'] += '%s<li>' % l
                    else:
                        block['html'] += '</li><li>'
                else:
                    if prev_list is not None:
                        block['html'] += '</li>'
                    self.__closeblock__(block, prev_list)
                    block['html'] += '<p>'


            html = self.__run2html__(run, r_index)
            if link:
                html = '<a href=\"%s\">%s</a>' % (link, html)
            if block['html'] == '':
                html = '<p>' + html

            block['html'] += html

            prev_paragraph = paragraph
            r_index += 1

        self.__closeblock__(block, this_list)

        return blocks

    def __closeblock__(self, block, last_list=None):
        if block is not None:
            if block['type'] == 'paragraph':
                if last_list is not None:
                    l = '</ul>' if last_list == 'unordered' else '</ol>'
                    block['html'] += l
                elif block['html'] != '':
                    block['html'] += '</p>'



    def __run2html__(self, run, r_index):

        if self.__runisfootnote__(run):
            self._footnoteindex+=1
            return '{{%s}}' % str(self._footnoteindex)

        text = self.__getruntext__(run, r_index)
        if run.italic:
            text = '<em>%s</em>' % text
        if run.bold:
            text = '<b>%s</b>' % text

        return text

    def __getruntext__(self, run, r_index):
        texts = run.element.findall('.//w:t', self._namespaces)
        text = ''
        for i, t in enumerate(texts):
            # never add breaks at start of paragraph
            if r_index > 0 or i > 0:
                prev_breaks = self.__countprevbreaks__(t)
                if prev_breaks == 1:
                    text += '<br/>'
                elif prev_breaks == 2:
                    text += '</p><p>'

            text += t.text

            # check for trailing breaks only at end
            if i < len(texts)-1: continue

            next_breaks = self.__countnextbreaks__(t)
            if next_breaks == 1:
                text += '<br/>'
            elif next_breaks == 2:
                text += '</p><p>'

        return text

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
        if p is None: return count
        if p.tag != breaktag: return count
        count += 1
        return self.__countprevbreaks__(p, count)

    def __getparagraphlist__(self, paragraph):
        if paragraph is None:
            return None
        elif paragraph._element.find('.//w:ilvl', self._namespaces) is not None:
            numId = paragraph._element.find('.//w:numId', self._namespaces)
            val = numId.get('{%s}val' % self._namespaces['w'])
            if val == '2':
                return 'ordered'
            else:
                return 'unordered'
        else:
            return None

    def __runisfigure__(self, run):
        if run.element.find('.//w:drawing', self._namespaces) is not None:
            return True

        return False

    def __runisfootnote__(self, run):
        if run.element.find('.//w:footnoteReference', self._namespaces) is not None:
            return True

        return False
