import smartypants
from django import template

register = template.Library()


@register.filter
def smart_quotes(text, should_apply=True):
    """Attempt to convert straight quotes to curly quotes with the
    smartypants library.  Does nothing if `should_apply` is `False`,
    which is needed to operate as a conditional filter in a Django
    template.

    """
    if not should_apply:
        return text

    # Prepare for application of smartypants by replacing Draftail's
    # quote entities with ASCII quotes.  Smartypants does not replace
    # entities by default.  The `Attr.w` argument also tells
    # smartypants to replace the `&quot;` entity.
    text = text.replace("&#x27;", "'")
    attrs = smartypants.Attr.w | smartypants.Attr.set1
    return smartypants.smartypants(text, attrs)
