from django import template

from home.models import Post
from programs.models import Program, AbstractProgram


register = template.Library()


@register.inclusion_tag('tags/side_menu.html', takes_context=True)
def side_menu(context, parent, calling_page=None):
    """ Returns the needed data to create the dynamic sidebar """
    page_depth = context['self'].depth
    if page_depth == 3:
        menu_program = context['self']
    elif page_depth > 3:
        program_name = context['self'].get_ancestors()[2]
        menu_program = Program.objects.get(title=program_name)
    context['side_menu'] = {}
    context['side_menu']['url'] = menu_program.url
    context['side_menu']['logo'] = menu_program.program_logo
    context['side_menu']['title'] = menu_program.title
    context['side_menu']['initiative_pages'] = menu_program.sidebar_menu_initiatives_and_projects_pages
    context['side_menu']['work_pages'] = menu_program.sidebar_menu_our_work_pages
    context['side_menu']['about_pages'] = menu_program.sidebar_menu_about_us_pages
    return context