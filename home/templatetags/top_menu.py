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
    # programs = Program.objects.in_menu().order_by("title").exclude(location=True)
    programs = []
    location_programs = []
    all_programs = Program.objects.in_menu().order_by("title")
    for program in all_programs:
        if program.location == True:
            location_programs.append(program)
        else:
            programs.append(program)

    return {
        'calling_page': calling_page,
        'programs': programs,
        'location_programs': location_programs,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs - will only add iniatives where show_in_menus field is set to true
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    subprograms_list = []

    for subprogram in parent.get_subprograms():
        if subprogram.show_in_menus:
            subprograms_list.append(subprogram)

    return {
        'parent': parent,
        'subprograms': subprograms_list,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

