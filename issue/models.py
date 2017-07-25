from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram, AbstractProgram

from home.models import Post, ProgramSimplePage

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, PageChooserPanel

from programs.models import Program

class TopicHomePage(Page):
    parent_page_types = ['programs.Program', 'home.HomePage']
    subpage_types = ['IssueOrTopic']

    class Meta:
        verbose_name = 'Topics'

class IssueOrTopic(ProgramSimplePage):
    parent_page_types = ['TopicHomePage', 'IssueOrTopic',]
    subpage_types = ['IssueOrTopic']

    parent_program = models.ForeignKey(
        'programs.Program',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='topics'
    )

    def get_context(self, request):
        context = super(IssueOrTopic, self).get_context(request)

        context['topics'] = self.get_children().live()

        return context

    def save(self, *args, **kwargs):
        program_page = self.get_ancestors()[2]
        if program_page:
            program = Program.objects.get(pk=program_page.id);
            self.parent_program = program
        super(IssueOrTopic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Topic'
