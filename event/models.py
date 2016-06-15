import json

from django.db import models
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from home.models import Post
from mysite.helpers import paginate_results, generate_url
from programs.models import Program, Subprogram
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page


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
            get_org_wide_events(self, request, tense="future")
        )

    @route(r'^past/$')
    def past_events(self, request):
        self.title = "Past " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_org_wide_events(self, request, tense="past")
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
            get_program_and_subprogram_events(self, request, tense="future")
        )

    @route(r'^past/$')
    def past_events(self, request):
        self.title = "Past " + self.title
        return TemplateResponse(
            request,
            self.get_template(request),
            get_program_and_subprogram_events(self, request, tense="past")
        )

    class Meta:
        verbose_name = "Events Homepage for Program and Subprograms"


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
        program_query = Q(parent_programs=int(search_program))

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
            subprogram_query = Q(post_subprogram=int(search_subprogram))

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
        date_range = json.loads(user_date_query)
        date_query = Q(date__range=(date_range['start'], date_range['end']))
    else:
        if tense == "future":
            # ensures that multi-day events are displayed on future events page until their end date has passed
            date_query = Q(date__gte=curr_date) | Q(end_date__gte=curr_date)
        else:
            # ensures that multi-day events are not displayed on past events page until their end date has passed
            date_query = Q(date__lt=curr_date) & (Q(end_date__isnull=True) | Q(end_date__lt=curr_date))

    return date_query
