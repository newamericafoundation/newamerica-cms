from datetime import date
from django import template
from django.conf import settings

from programs.models import Program, AbstractProgram
from event.models import AllEventsHomePage
from home.models import Post

register = template.Library()


@register.assignment_tag(takes_context=True)
def needs_sidebar(context):
    """ Returns false if sidebar is not required """
    use_side_bar = False
    self_context = context.get('self')
    
    if context.get('show_sidebar'):
        use_side_bar = True
    
    if self_context:
        if isinstance(self_context, Post):
            use_side_bar = True
        elif 'programs.Program' in self_context.parent_page_types:
            use_side_bar = True
        elif isinstance(self_context, AbstractProgram):
            use_side_bar = True
    return use_side_bar

# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag('tags/side_menu.html', takes_context=True)
def side_menu(context, parent, calling_page=None):
    # # programs = Program.objects.in_menu().order_by("title").exclude(location=True)
    # programs = []
    # location_programs = []
    # all_programs = Program.objects.in_menu().order_by("title")
    # for program in all_programs:
    #     if program.location == True:
    #         location_programs.append(program)
    #     else:
    #         programs.append(program)
    # return {
    #     'calling_page': calling_page,
    #     # 'programs': programs,
    #     # 'location_programs': location_programs,
    #     # required by the pageurl tag that we want to use within this template
    #     'request': context['request'],
    # }
    return {}


# Retrieves the children of the top menu items for the drop downs
# @register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
# def top_menu_children(context, parent):
#     subprograms = parent.subprogram_set.all()

#     return {
#         'parent': parent,
#         'subprograms': subprograms,
#         # required by the pageurl tag that we want to use within this template
#         'request': context['request'],
#     }
