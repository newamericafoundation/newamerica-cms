NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
}

TAGS = {
    '{%s}r' % NAMESPACES['w']: 'run',
    '{%s}hyperlink' % NAMESPACES['w']: 'hyperlink',
    '{%s}pPr' % NAMESPACES['w']: 'break'
}
