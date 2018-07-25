from .blocks import group_elements_into_blocks
from .parsers import convert_table_child

class Section():
    def __init__(self, heading, doc, links, endnotes):
        self._doc = doc
        self._links = links
        self.endnotes = endnotes
        # docx type: Paragraph
        self._paragraph = heading
        self.title = heading.text
        self._paragraphs = []
        self._elements = []
        self.blocks = []

    def add_paragraph(self, paragraph):
        self._paragraphs.append(paragraph)
        # sometimes something that should be a single wagtail block
        # spans multiple docx Paragraphs
        # flatten structure then compile elements into blocks
        # so <section><Paragraph><elements></Paragraph></section>
        # is <section><elements></section>
        for c in paragraph._element.getchildren():
            self._elements.append((c,paragraph))

        self.__addtable__(paragraph)

    def __addtable__(self, paragraph):
        # docx excludes table elements when parsing Paragraphs,
        # check if next element is table, and add it to element
        next = paragraph._element.getnext();
        if next:
            tbl = convert_table_child(next, self._doc)
            if tbl:
                self._elements.append((tbl, paragraph))

    def compile_blocks(self):
        blocks = group_elements_into_blocks(self._elements, self)
        for b in blocks:
            b.compile_data()
            if b.skip:
                continue
            self.blocks.append(b.data)
