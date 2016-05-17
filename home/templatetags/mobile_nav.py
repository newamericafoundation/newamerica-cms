from django import template

from home.models import Post
from programs.models import Program, AbstractProgram


register = template.Library()


@register.inclusion_tag('tags/mobile_nav.html', takes_context=True)
def mobile_nav_secondary(context, parent, calling_page=None):
    page_depth = context['self'].depth
    if page_depth == 3:
        menu_program = context['self']
    elif page_depth > 3:
        program_name = context['self'].get_ancestors()[2]
        menu_program = Program.objects.get(title=program_name)

    context['mobile_logo'] = menu_program.mobile_program_logo
    context['program_name'] = menu_program.title

    return context