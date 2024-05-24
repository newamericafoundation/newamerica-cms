from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def social_media_icon_name(name):
    """Returns a corrected social media icon name usable as a font
    awesome class name, prefixed by `fa-`.  This is needed in cases
    where a human-readable or legacy descriptor of the social media
    brand does not match the current font awesome identifier.

    """
    mappings = {
        'facebook': 'facebook-f',
        'twitter': 'x-twitter',
        'google_plus': 'google-plus-g',
    }
    prefix = 'fa'
    adjusted_name = mappings.get(name, name)
    return f'{prefix}-{adjusted_name}'
