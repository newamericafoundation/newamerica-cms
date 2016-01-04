from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from programs.models import Program

from django.utils import timezone
from django.utils.timezone import now


class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    parent_page_types = ['ProgramEventsPage']
    subpage_types = []

    time = models.TimeField(default=timezone.now)
    address = models.TextField()
    rsvp_link = models.URLField()

    content_panels = Post.content_panels + [
        FieldPanel('time'),
        FieldPanel('rsvp_link'),
        FieldPanel('address'),
    ]


class AllEventsHomePage(Page):
    """
    Page which inherits from abstract Page model and returns every
    Event in the Event model for the Events homepage
    """
    parent_page_types = ['home.HomePage',]
    subpage_types = []

    def get_context(self, request):
        context = super(AllEventsHomePage, self).get_context(request)

        context['events'] = Event.objects.all()
        return context

    class Meta:
        verbose_name = "Homepage for all Events"


class ProgramEventsPage(Page):
    """
    Page which inherits from abstract Page model and returns every
    Event associated with a specific Program which is determined
    using the url path
    """
    parent_page_types = ['programs.Program',]
    subpage_types = ['Event']

    def get_context(self, request):
        context = super(ProgramEventsPage, self).get_context(request)
        program_slug = request.path.split("/")[-3]
        program = Program.objects.get(slug=program_slug)
        context['events'] = Event.objects.filter(parent_programs=program)
        context['program'] = program
        return context

    class Meta:
        verbose_name = "Events Homepage for Program"

