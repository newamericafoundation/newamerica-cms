from docx.text.run import Run
from .parsers import (
    parse_paragraph, parse_table, parse_list,
    parse_hyperlink, parse_break, parse_footnote
)
from .block_utils import *
from .settings import TAGS

class NestedElement(object):
    def __init__(self, type):
        self.type = type
        self._elements = []

    def add_element(self, element):
        self._elements.append(element)

class Block(object):
    def __init__(self, type, section):
        self.type = type
        self._elements = []
        self.section = section
        self.skip = False
        self._nested_element = None
        self.data = {
            'type': type
        }

    def add_element(self, element):
        if self._nested_element:
            self._elements.append(self._nested_element)
            self._nested_element = None

        self._elements.append(element)

    def add_nested_element(self, type, element):
        # Primarily for paragraph blocks,
        # nested elements should be grouped and parsed separately
        # from top level elements
        # ex: lists, hyperlinks, footnotes
        if self._nested_element == None:
            self._nested_element = NestedElement(type)
        elif self._nested_element.type != type:
            self._elements.append(self._nested_element)
            self._nested_element = NestedElement(type)

        self._nested_element.add_element(element)

    def compile_data(self):
        pass

class BoxBlock(Block):
    def __init__(self, type, section):
        super(BoxBlock, self).__init__(type, section)
        self.data = {
            'type': 'box',
            'blocks': []
        }

        self.blocks = []

    def compile_data(self):
        blocks = group_elements_into_blocks(self._elements, self.section)
        for b in blocks:
            b.compile_data()
            if b.type == 'table':
                # not a think yet
                continue
            self.data['blocks'].append(b.data)

class HeadingBlock(Block):
    def __init__(self, type, section):
        super(HeadingBlock, self).__init__(type, section)
        self.data = {
            'type': type,
            'data': []
        }

    def compile_data(self):
        text = ''
        for child, paragraph in self._elements:
            run = Run(child, paragraph)
            text += run.text

        self.data['text'] = text

class TableBlock(Block):
    def __init__(self, type, section):
        super(TableBlock, self).__init__(type, section)
        self.data = {
            'type': type,
            'data': []
        }

    def compile_data(self):
        child, paragraph = self._elements[0]
        self.data['data'] = parse_table(child, self.section)


class InlineImageBlock(Block):
    def __init__(self, type, section):
        super(InlineImageBlock, self).__init__(type, section)
        self.data = {
            'type': type,
            'box': None
        }

class ParagraphBlock(Block):
    def __init__(self, type, section):
        super(ParagraphBlock, self).__init__(type, section)
        self.data = {
            'type': type,
            'html': ''
        }

    def compile_data(self):
        html = '<p>'
        for i, el in enumerate(self._elements):
            if type(el) == NestedElement:
                if el.type == 'list':
                    html_ = parse_list(el, self.section)
                elif el.type == 'hyperlink':
                    html_ = parse_hyperlink(el, self.section)
                elif el.type == 'footnote':
                    html_ = parse_footnote(el)
                elif el.type == 'break':
                    html_ = parse_break(el, html)
            else:
                child, paragraph = el
                run = Run(child, paragraph)
                html_ = parse_paragraph(run, paragraph)

            html += html_

        html += '</p>'
        self.data['html'] = html.replace('<p></p>', '')
        if self.data['html'] == '':
            self.skip = True

def group_elements_into_blocks(elements, section):
    blocks = []
    block = None
    curr_runtype = None
    prev_runtype = None
    for el in elements:
        child, paragraph = el
        block_type, curr_runtype, nested_element_type, attrs = get_block_type(child, paragraph)

        if curr_runtype == None:
            continue

        if curr_runtype != prev_runtype and block_type != None and prev_runtype != 'boxstart':
            block = block_type(curr_runtype, section)
            blocks.append(block)

        if curr_runtype not in ['boxstart', 'boxend']:
            if nested_element_type and prev_runtype != 'boxstart':
                if nested_element_type == 'hyperlink':
                    # move down a level to get run child of hyperlink
                    child = child.find('.//w:r', NAMESPACES)
                block.add_nested_element(nested_element_type, (child, paragraph, attrs))
            else:
                block.add_element(el)

        if prev_runtype != 'boxstart' or (prev_runtype == 'boxstart' and curr_runtype == 'boxend'):
            prev_runtype = curr_runtype

    return blocks

def get_block_type(child,paragraph):
    type_ = type(child)

    if type_ == Table:
        return (TableBlock, 'table', None, None)

    tag = TAGS.get(child.tag, None)
    run = Run(child, paragraph)
    list = paragraphlisttype(paragraph)
    isbreak = childisbreak(child)
    hyperlink = childishyperlink(child)
    footnote = runisfootnote(run)

    if tag is None:
        return (None, None, None, None)
    elif runisfigure(run):
        return (InlineImageBlock, 'inline_image', None, None)
    elif isbreak and not list:
        return (ParagraphBlock, 'paragraph', 'break', None)
    elif list and not isbreak:
        return (ParagraphBlock, 'paragraph', 'list', list)
    elif isbreak:
        return (None, None, None, None)
    elif run.text == '' and not runisfootnote(run):
        return (None, None, None, None)
    elif hyperlink:
        return (ParagraphBlock, 'paragraph', 'hyperlink', hyperlink)
    elif paragraph.style.name == 'Heading 2':
        if runisboxstart(run):
            return (BoxBlock, 'boxstart', None, None)
        if runisboxend(run):
            return (None, 'boxend', None, None)
        else:
            return (HeadingBlock, 'heading', None, None)
    elif footnote:
        return (ParagraphBlock, 'paragraph', 'footnote', footnote)
    else:
        return (ParagraphBlock, 'paragraph', None, None)
