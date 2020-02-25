from __future__ import unicode_literals
import json

from home.models import Post

from wagtail.core.models import Page, PageRevision
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.blocks import PageChooserBlock

from programs.models import AbstractContentPage
from newamericadotorg.helpers import paginate_results
from home.models import AbstractHomeContentPage

class Weekly(AbstractContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = ['WeeklyArticle']

    def get_context(self, request):
        context = super(Weekly, self).get_context(request)

        context['latest_edition'] = WeeklyEdition.objects.live().public().first()
        if getattr(request, 'is_preview', False):
            edition_context = context['latest_edition'].get_context(request)
            context['initial_state'] = edition_context['initial_state']

        return context

    class Meta:
        verbose_name = "Weekly Editions"


class WeeklyEdition(Page):
    parent_page_types = []
    subpage_types = []

    def get_context(self, request):
        context = super().get_context(request)
        if getattr(request, 'is_preview', False):
            import newamericadotorg.api.weekly
            revision = PageRevision.objects.filter(page=self).last().as_page_object()
            weekly_data = newamericadotorg.api.weekly.serializers.WeeklyEditionSerializer(revision, context={'is_preview': True}).data
            context['initial_state'] = json.dumps(weekly_data)

        return context


class WeeklyArticle(Post):
    parent_page_types = ['Weekly']
    subpage_types = []

    def get_context(self, request):
        context = super(WeeklyArticle, self).get_context(request)
        context['edition'] = self.get_parent().specific

        if getattr(request, 'is_preview', False):
            edition_context = context['edition'].get_context(request)
            context['initial_state'] = edition_context['initial_state']

        return context

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Weekly Article'


class AllWeeklyArticlesHomePage(AbstractHomeContentPage):
    parent_page_types = ['home.HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Weekly Articles Homepage'

    @property
    def content_model(self):
        return WeeklyArticle
