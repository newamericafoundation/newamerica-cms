import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import QueryDict
from django.db.models import Q

from datetime import datetime, timedelta
from pytz import timezone

from programs.models import Program, Subprogram

def paginate_results(request, all_posts):
    page = request.GET.get('page')
    paginator = Paginator(all_posts, 12)
    
    try:
        all_posts = paginator.page(page)
    except PageNotAnInteger:
        all_posts = paginator.page(1)
    except EmptyPage:
        all_posts = paginator.page(paginator.num_pages)

    return all_posts


def get_org_wide_posts(self, request, page_type, content_model):
    """
    Function to return a list of content 
    for org wide content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(page_type, self).get_context(request)

    search_program = request.GET.get('program_id', None)
    date = request.GET.get('date', None)

    filter_dict = {}

    if search_program:
        filter_dict['parent_programs'] = int(search_program)
    if date:
        date_range = json.loads(date)
        filter_dict['date__range'] = (date_range['start'], date_range['end'])   

    all_posts = content_model.objects.filter(**filter_dict)
    context['all_posts'] = paginate_results(request, all_posts.live().order_by("-date"))
    context['programs'] = Program.objects.all().live().in_menu().order_by('title')
    context['query_url'] = generate_url(request)
    
    return context

def get_org_wide_events(self, request, page_type, content_model, tense):
    """
    Function to return a list of content 
    for org wide content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(page_type, self).get_context(request)

    search_program = request.GET.get('program_id', None)
    date = request.GET.get('date', None)

    date_query = Q()
    program_query = Q()
    
    if search_program:
        program_query = Q(parent_programs__exact=int(search_program))
    
    if date:
        date_range = json.loads(date)
        date_query = Q(date__range=(date_range['start'], date_range['end']))
    else:
        date_query = set_default_date_query(tense)
    
    all_events = content_model.objects.filter(date_query & program_query)
    if (tense == "future"):
        context['all_events'] = paginate_results(request, all_events.live().order_by("date", "start_time"))
    else:
        context['all_events'] = paginate_results(request, all_events.live().order_by("-date", "-start_time"))
    
    context['programs'] = Program.objects.all().live().in_menu().order_by('title')
    context['query_url'] = generate_url(request)

    return context


def get_program_and_subprogram_posts(self, request, page_type, content_model):
    """
    Function to return a list of content for a program or 
    subprogram content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """
    context = super(page_type, self).get_context(request)

    search_subprogram = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)

    # program grid
    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)

        filter_dict = {'parent_programs': program}
        if search_subprogram:
            filter_dict['post_subprogram'] = int(search_subprogram)
        if date:
            date_range = json.loads(date)
            filter_dict['date__range'] = (date_range['start'], date_range['end'])
    
        all_posts = content_model.objects.live().filter(**filter_dict)
        context['subprograms'] = program.get_children().type(Subprogram).live().order_by('title')
    # subprogram_grid
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)
        all_posts = content_model.objects.live().filter(post_subprogram=program)

    context['all_posts'] = paginate_results(request, all_posts.order_by("-date"))
    context['all_events'] = paginate_results(request, all_posts.live().order_by("date", "start_time"))

    context['program'] = program
    context['query_url'] = generate_url(request)
    
    return context

def get_program_and_subprogram_events(self, request, page_type, content_model, tense):
    """
    Function to return a list of content for a program or 
    subprogram content homepage.

    Also checks if there is a query to filter content by initiatives
    or by date for programs.
    """

    print("in get programs and subprograms!")
    context = super(page_type, self).get_context(request)

    search_subprogram = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)

    date_query = Q()
    program_query = Q()
    subprogram_query = Q()

    # if program grid
    if self.depth == 4:
        program_title = self.get_ancestors()[2]
        program = Program.objects.get(title=program_title)

        program_query = Q(parent_programs__exact=program)
        if search_subprogram:
            subprogram_query = Q(post_subprogram__exact=int(search_subprogram))

        context['subprograms'] = program.get_children().type(Subprogram).live().order_by('title')
    # if subprogram grid
    else:
        subprogram_title = self.get_ancestors()[3]
        program = Subprogram.objects.get(title=subprogram_title)

        subprogram_query = Q(post_subprogram__exact=int(search_subprogram))

    if date:
        date_range = json.loads(date)
        date_query = Q(date__range=(date_range['start'], date_range['end']))
    else:
        date_query = set_default_date_query(tense)

    all_events = content_model.objects.live().filter(date_query & program_query & subprogram_query)
    print("here!")
    print(all_events)
    if (tense == "future"):
        context['all_events'] = paginate_results(request, all_events.live().order_by("date", "start_time"))
    else:
        context['all_events'] = paginate_results(request, all_events.live().order_by("-date", "-start_time"))

    context['program'] = program
    context['query_url'] = generate_url(request)
    
    return context

def set_default_date_query(tense):
    datetime_format = "%Y-%m-%d"
    eastern = timezone('US/Eastern')
    curr_date = datetime.now(eastern).date().strftime(datetime_format)

    if (tense == "future"):
        return Q(date__gte=curr_date) | Q(end_date__gte=curr_date)
    else:
        return Q(date__lt=curr_date) & (Q(end_date__isnull=True) | Q(end_date__lt=curr_date))

def generate_url(request):
    query = QueryDict(mutable=True)
    program_id = request.GET.get("program_id", None)
    subprogram_id = request.GET.get('subprogram_id', None)
    date = request.GET.get('date', None)
    if program_id:
        query['program_id'] = program_id
    if date:
        query['date'] = date
    if subprogram_id:
        query['subprogram_id'] = subprogram_id

    return query.urlencode()