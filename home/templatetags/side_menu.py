from datetime import date
from django import template
from django.conf import settings

from wagtail.wagtailcore.models import Page

from programs.models import Program, AbstractProgram, Subprogram

from event.models import AllEventsHomePage

from home.models import Post, SimplePage

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

# Retrieves the top menu items - the immediate children of the parent page
@register.inclusion_tag('tags/side_menu.html', takes_context=True)
def side_menu(context, parent, calling_page=None):
   
    def build_menu():
        # if page_depth == 3:
        #     menu_program = context['self']
        # elif page_depth == 4:
        #     program_name = context['self'].get_parent()
        #     menu_program = Program.objects.get(title=program_name)
        # elif page_depth == 5: 
        #     program_name = context['self'].get_parent().get_parent()
        #     menu_program = Program.objects.get(title=program_name)
        page_depth = context['self'].depth
        
        if page_depth == 3:
            menu_program = context['self']
        elif page_depth > 3:
            program_name = context['self'].get_ancestors()[2]
            menu_program = Program.objects.get(title=program_name)

        context['url'] = menu_program.url
        context['logo'] = menu_program.title
        context['initiative_pages'] = menu_program.sidebar_menu_initiatives_and_projects_pages
        context['work_pages'] = menu_program.sidebar_menu_our_work_pages
        context['about_pages'] = menu_program.sidebar_menu_about_us_pages

        return context
    
    build_menu()

    return context