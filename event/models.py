from django.db import models

from home.models import Post

from wagtail.wagtailcore.models import Page
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import FieldPanel

from django.template.response import TemplateResponse
from django.utils import timezone

from mysite.helpers import paginate_results, get_program_and_subprogram_events, get_org_wide_events


class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    parent_page_types = ['ProgramEventsPage']
    subpage_types = []

    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now, blank=True, null=True)
    host_organization = models.TextField(
        default='New America', 
        blank=True, 
        null=True
    )
    street_address = models.TextField(default='740 15th St NW #900')
    city = models.TextField(default='Washington')
    state = models.TextField(default='D.C.')
    zipcode = models.TextField(default='20005')
    rsvp_link = models.URLField(default='http://www.')
    soundcloud_url = models.URLField(blank=True, null=True)

    content_panels = Post.content_panels + [
        FieldPanel('end_date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('rsvp_link'),
        FieldPanel('host_organization'),
        FieldPanel('street_address'),
        FieldPanel('city'),
        FieldPanel('state'),
        FieldPanel('zipcode'),
        FieldPanel('soundcloud_url'),
    ]


class AllEventsHomePage(RoutablePageMixin, Page):
    """
    Page which inherits from abstract Page model and returns every
    Event in the Event model for the Events homepage
    """
    parent_page_types = ['home.HomePage']
    subpage_types = ['Event']

    @route(r'^$')
    def future_events(self, request):
        self.title = "Future " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_org_wide_events(self, request, AllEventsHomePage, Event, "future")
        )

    @route(r'^past/$')
    def past_events(self, request):
        self.title = "Past " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_org_wide_events(self, request, AllEventsHomePage, Event, "past")
        )

    class Meta:
        verbose_name = "Homepage for all Events"


class ProgramEventsPage(RoutablePageMixin, Page):
    """
    Page which inherits from abstract Page model and returns every
    Event associated with a specific Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram']
    subpage_types = ['Event']

    @route(r'^$')
    def future_events(self, request):
        self.title = "Future " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_program_and_subprogram_events(self, request, ProgramEventsPage, Event, "future")
        )

    @route(r'^past/$')
    def past_events(self, request):
        self.title = "Past " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_program_and_subprogram_events(self, request, ProgramEventsPage, Event, "past")
        )

    class Meta:
        verbose_name = "Events Homepage for Program and Subprograms"

