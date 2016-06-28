from datetime import date
from django import template
from django.conf import settings

from programs.models import Program

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag('tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    all_programs = Program.objects.in_menu().order_by("title").exclude(location=True)
    location_programs = Program.objects.in_menu().order_by("title").filter(location=True)

    return {
        'calling_page': calling_page,
        'programs': all_programs,
        'locations': location_programs,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    subprograms = parent.get_subprograms

    return {
        'parent': parent,
        'subprograms': subprograms,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

