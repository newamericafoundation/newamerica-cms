from docx.text.run import Run
from docx.table import Table

from .settings import NAMESPACES, TAGS

def runisfigure(run):
    if run.element.find('.//w:drawing', NAMESPACES) is not None:
        return True

    return False

def runisfootnote(run):
    footnote = run.element.find('.//w:footnoteReference', NAMESPACES)
    if footnote is not None:
        return footnote.get('{%s}id' % NAMESPACES['w'])

    return False

def runisboxstart(run):
    text = run.text.lower().strip()
    if text in ['box', 'boxstart', 'box start', 'startbox', 'start box']:
        return True
    return False

def runisboxend(run):
    text = run.text.lower().strip()
    if text in ['end box', 'endbox', 'box end', 'boxend']:
        return True
    return False

def childisbreak(child):
    return TAGS.get(child.tag, None) == 'break'

def childishyperlink(child):
    if TAGS.get(child.tag, None) == 'hyperlink':
        # return linkId
        return child.get('{%s}id' % NAMESPACES['r'])
    return False

def paragraphlisttype(paragraph):
    if paragraph is None:
        return False
    elif paragraph._element.find('.//w:ilvl', NAMESPACES) is not None:
        ilvl = paragraph._element.find('.//w:ilvl', NAMESPACES)
        level = ilvl.get('{%s}val' % NAMESPACES['w'])
        numId = paragraph._element.find('.//w:numId', NAMESPACES)
        val = numId.get('{%s}val' % NAMESPACES['w'])
        if val == '2':
            return ('ol', level)
        else:
            return ('ul', level)
    else:
        return False
