from django import template
import re
from wagtail.core.rich_text import RichText

register = template.Library()

@register.filter()
def cited_html(html):
    if type(html) == RichText:
        html = html.__html__()
    elif type(html) != str:
        html = str(html)

    match = re.search('\{\{([0-9]+)\}\}', html)

    if match is None:
        return html

    number = match.groups()[0]
    citation = '<span class="report__citation" data-citation-number="%s"><span class="citation-number">%s</span><span class="icon-plus x white"><span></span><span></span></span></span>' % (number, number)
    html = html.replace(match.group(), citation)
    return cited_html(html)

@register.filter()
def markdown_link(html):
    if type(html) == RichText:
        html = html.__html__()
    elif type(html) != str:
        html = str(html)

    name_regex = "[^]]+"
    # http:// or https:// followed by anything but a closing paren
    url_regex = "http[s]?://[^)]+"

    markup_regex = '\[({0})]\(\s*({1})\s*\)'.format(name_regex, url_regex)

    match = re.search(markup_regex, html)

    if match is None:
        return html

    group = match.groups()
    link = '<a href="%s">%s</a>' % (group[1], group[0])
    html = html.replace(match.group(), link)
    return markdown_link(html)
