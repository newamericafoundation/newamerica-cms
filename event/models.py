import json
from datetime import date

from django.db import models
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now

from programs.models import Program, Subprogram
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, PageChooserPanel
from wagtail.models import Page
from wagtail.fields import RichTextField

from home.models import Post
from conference.models import Conference
from newamericadotorg.helpers import paginate_results, generate_url, is_json, is_int
from programs.models import AbstractContentPage

class Event(Post):
    """
    Event class that inherits from the abstract Post
    model and creates pages for Events.
    """
    parent_page_types = ['ProgramEventsPage']
    subpage_types = []

    related_conference = models.ForeignKey(
        Conference,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now, blank=True, null=True)
    host_organization = models.TextField(
        default='New America',
        blank=True,
    )
    street_address = models.TextField(default='740 15th St NW #900', blank=True)
    city = models.TextField(default='Washington', blank=True)
    state = models.TextField(default='DC', blank=True)
    zipcode = models.TextField(default='20005', blank=True)
    online_only = models.BooleanField(default=False, help_text="Checking this will mean the address is not shown")
    webcast_url = models.URLField(blank=True)
    webcast_link_text = models.TextField(blank=True, help_text="Defaults to 'Webcast link'")
    rsvp_link = models.URLField(blank=True)
    soundcloud_url = models.URLField(blank=True, null=True)

    content_panels = Post.content_panels + [
        PageChooserPanel('related_conference', ['conference.Conference']),
        FieldPanel('end_date'),
        FieldPanel('start_time'),
        FieldPanel('end_time'),
        FieldPanel('rsvp_link'),
        FieldPanel('host_organization'),
        MultiFieldPanel([
            FieldPanel('online_only'),
            FieldPanel('street_address'),
            FieldPanel('city'),
            FieldRowPanel([
                FieldPanel('state', classname='col6'),
                FieldPanel('zipcode', classname='col6')
            ])
        ], heading='Location'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('webcast_url'),
                FieldPanel('webcast_link_text'),
            ])
        ], heading='Webcast link'),
        FieldPanel('soundcloud_url'),
    ]

    @property
    def is_past(self):
        return date.today() > self.date

    class Meta:
        verbose_name = 'Event'


class AllEventsHomePage(RoutablePageMixin, AbstractContentPage):
    """
    Page which inherits from abstract Page model and returns every
    Event in the Event model for the Events homepage
    """
    parent_page_types = ['home.HomePage']
    subpage_types = ['Event']

    body = RichTextField(blank=True)

    content_panels = AbstractContentPage.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Events Homepage"


class ProgramEventsPage(RoutablePageMixin, AbstractContentPage):
    """
    Page which inherits from abstract Page model and returns every
    Event associated with a specific Program or Subprogram
    """
    parent_page_types = ['programs.Program', 'programs.Subprogram', 'programs.Project']
    subpage_types = ['Event']

    class Meta:
        verbose_name = "Events Homepage"


def get_org_wide_events(self, request, tense):
    """
    Function to return a list of events
    for org wide events homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(AllEventsHomePage, self).get_context(request)

    search_program = request.GET.get('program_id', None)
    date = request.GET.get('date', None)

    program_query = Q()
    date_query = set_events_date_query(date, tense)

    if search_program:
        if is_int(search_program):
            program_query = Q(parent_programs=int(search_program))
        else:
            program_query = Q(id__isnull=True)

    all_events = Event.objects.filter(date_query & program_query)

    if tense == "future":
        context['all_events'] = paginate_results(request, all_events.live().order_by("date", "start_time"))
    else:
        context['all_events'] = paginate_results(request, all_events.live().order_by("-date", "-start_time"))

    context['programs'] = Program.objects.all().live().in_menu().order_by('title')
    context['query_url'] = generate_url(request)

    return context


def get_program_and_subprogram_events(self, request, tense):
    """
    Function to return a list of events for a program or
    subprogram events homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """

    context = super(ProgramEventsPage, self).get_context(request)

    search_subprogram = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)

    program_query = Q()
    subprogram_query = Q()
    date_query = set_events_date_query(date, tense)

    # if program
    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)
        program_query = Q(parent_programs=program)
        if search_subprogram:
            if is_int(search_subprogram):
                subprogram_query = Q(post_subprogram=int(search_subprogram))
            else:
                subprogram_query = Q(id__isnull=True)

        context['subprograms'] = program.get_children().type(Subprogram).live().order_by('title')
    # if subprogram
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)
        subprogram_query = Q(post_subprogram=program)

    all_events = Event.objects.live().filter(date_query & program_query & subprogram_query)

    if (tense == "future"):
        context['all_events'] = paginate_results(request, all_events.live().order_by("date", "start_time"))
    else:
        context['all_events'] = paginate_results(request, all_events.live().order_by("-date", "-start_time"))
    context['query_url'] = generate_url(request)
    context['program'] = program

    return context

def set_events_date_query(user_date_query, tense):
    """
    Function to generate date query for events -
    If user date query exists, sets this as date range query parameter,
    else defaults to greater than current date for future, and less than current date for past
    """
    curr_date = localtime(now()).date()

    if user_date_query:
        if is_json(user_date_query):
            date_range = json.loads(user_date_query)
            if isinstance(date_range, dict):
                if 'start' in date_range and 'end' in date_range:
                    date_query = Q(date__range=(date_range['start'], date_range['end']))
                else:
                    date_query = Q(id__isnull=True)
            else:
                date_query = Q(id__isnull=True)
        else:
            date_query = Q(id__isnull=True)
    else:
        if tense == "future":
            # ensures that multi-day events are displayed on future events page until their end date has passed
            date_query = Q(date__gte=curr_date) | Q(end_date__gte=curr_date)
        else:
            # ensures that multi-day events are not displayed on past events page until their end date has passed
            date_query = Q(date__lt=curr_date) & (Q(end_date__isnull=True) | Q(end_date__lt=curr_date))

    return date_query
