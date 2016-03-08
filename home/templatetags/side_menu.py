from django import template

from home.models import Post
from programs.models import Program, AbstractProgram


register = template.Library()


@register.assignment_tag(takes_context=True)
def needs_sidebar(context):
    """ Checks if the page is an AbstractProgram descendant """
    use_side_bar = False
    if isinstance(context['self'], AbstractProgram):
        use_side_bar = True
    elif isinstance(context['self'], Post):
        use_side_bar = True
    elif 'programs.Program' in context['self'].parent_page_types:
        use_side_bar = True
    return use_side_bar


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
    context['side_menu']['logo'] = menu_program.title
    context['side_menu']['initiative_pages'] = menu_program.sidebar_menu_initiatives_and_projects_pages
    context['side_menu']['work_pages'] = menu_program.sidebar_menu_our_work_pages
    context['side_menu']['about_pages'] = menu_program.sidebar_menu_about_us_pages
    return context