from __future__ import unicode_literals

from django.db import models
from programs.models import Program, Subprogram

from home.models import Post, ProgramSimplePage

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from programs.models import Program


class IssueOrTopic(ProgramSimplePage):
    parent_page_types = ['programs.Program', 'IssueOrTopic', 'programs.Subprogram']
    subpage_types = ['IssueOrTopic']

    def get_context(self, request):
        context = super(IssueOrTopic, self).get_context(request)

        context['topics'] = self.get_children().live()

        return context
