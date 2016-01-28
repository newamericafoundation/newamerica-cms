from __future__ import unicode_literals

from django.db import models
from programs.models import Program, Subprogram

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from programs.models import Program


class Issue(Post):
	"""
	Issue class that inherits from the abstract Post
	model and creates pages for Issues.
	"""
	parent_page_types = ['ProgramIssuesPage',]
	subpage_types = []


class ProgramIssuesPage(Page):
    parent_page_types = ['programs.Program',]
    subpage_types = ['Issue']

    def get_context(self, request):
        context = super(ProgramIssuesPage, self).get_context(request)
        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        issues = Issue.objects.filter(parent_programs=program)
        context['issues'] = issues
        context['program'] = program
        
        return context

    class Meta:
        verbose_name = "Issues Homepage for Program"
