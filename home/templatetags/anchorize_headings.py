from collections import Counter

from django import template
from django.utils.text import slugify
from lxml import etree, html

register = template.Library()


@register.filter
def anchorize_headings(value):
    ids = Counter()

    try:
        root = html.fragment_fromstring(value, create_parent="div")
    except etree.ParserError:
        return value

    headings = root.xpath("//h1|//h2|//h3|//h4|//h5|//h6")
    if not headings:
        return value

    for heading in headings:
        slug_id = slugify(heading.text_content())
        if ids[slug_id]:
            anchor = "{}-{}".format(slug_id, ids[slug_id])
        else:
            anchor = slug_id
        ids[slug_id] += 1
        heading.attrib["id"] = anchor

    return "".join(map(fragment_to_string, root))


def fragment_to_string(fragment):
    return html.tostring(fragment).decode("utf-8")
