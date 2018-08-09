from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from programs.models import Program, Subprogram, AbstractProgram, AbstractContentPage

from home.models import Post, ProgramSimplePage

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel

from programs.models import Program

class TopicHomePage(AbstractContentPage):
    parent_page_types = ['programs.Program', 'home.HomePage']
    subpage_types = ['IssueOrTopic']

    def get_template(self, request):
        return 'programs/program.html'

    def get_context(self, request):
        context = super(IssueOrTopic, self).get_context(request)
        context['program'] = self.get_ancestors()[2].specific

        if request.is_preview:
            program_context = context['program'].get_context(request)
            context['initial_state'] = program_context['initial_state']
            context['initial_topics_state'] = program_context['initial_topics_state']

        return context

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

    def get_template(self, request):
        return 'programs/program.html'

    def get_context(self, request):
        context = super(IssueOrTopic, self).get_context(request)
        context['topics'] = self.get_children().live()
        ancestors = self.get_ancestors()
        if len(ancestors) == 4:
            context['parent_topic'] = self
        elif len(ancestors) < 4:
            context['parent_topic'] = None
        else:
            context['parent_topic'] = ancestors[4]

        context['program'] = ancestors[2].specific

        if request.is_preview:
            program_context = context['program'].get_context(request)
            context['initial_state'] = program_context['initial_state']
            context['initial_topics_state'] = program_context['initial_topics_state']

        return context

    def save(self, *args, **kwargs):
        program_page = self.get_ancestors()[2]
        if program_page:
            program = Program.objects.get(pk=program_page.id);
            self.parent_program = program
        super(IssueOrTopic, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Topic'
