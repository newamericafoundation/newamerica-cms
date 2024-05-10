from django.urls import re_path

import newamericadotorg.api.author.views as author_views
import newamericadotorg.api.event.views as event_views
import newamericadotorg.api.home.views as home_views
import newamericadotorg.api.jobs.views as jobs_views
import newamericadotorg.api.meta.views as meta_views
import newamericadotorg.api.post.views as post_views
import newamericadotorg.api.program.views as program_views
import newamericadotorg.api.report.views as report_views
import newamericadotorg.api.search.views as search_views
import newamericadotorg.api.subscribe.views as subscribe_views
import newamericadotorg.api.survey.views as survey_views
import newamericadotorg.api.the_thread.views as thread_views
import newamericadotorg.api.topic.views as topic_views
import newamericadotorg.api.weekly.views as weekly_views

api_urls = [
    re_path(r'^post/$', post_views.PostList.as_view(), name='post_list'),
    re_path(r'^search/$', search_views.SearchList.as_view()),
    re_path(r'^search/programs/$', search_views.SearchPrograms.as_view()),
    re_path(r'^search/upcoming_events/$', search_views.SearchUpcomingEvents.as_view()),
    re_path(r'^search/pubs_and_past_events/$', search_views.SearchPublicationsAndPastEvents.as_view()),
    re_path(r'^search/people/$', search_views.SearchPeople.as_view()),
    re_path(r'^search/other/$', search_views.SearchOtherPages.as_view()),
    re_path(r'^event/$', event_views.EventList.as_view()),
    #url(r'^api/author/$', cache_page(60 * 10, key_prefix='author_list')(api_views.AuthorList.as_view()), name='author_list'),
    re_path(r'^author/$', author_views.AuthorList.as_view(), name='author_list'),
    #url(r'^api/fellow/$', cache_page(60 * 10, key_prefix='fellow_list')(api_views.FellowList.as_view())),
    re_path(r'^fellow/$', author_views.FellowList.as_view()),
    #url(r'^api/program/(?P<pk>[\d]+)/$', cache_page(60 * 1440, key_prefix='program_page')(api_views.ProgramDetail.as_view()), name='program'),
    re_path(r'^program/(?P<pk>[\d]+)/featured/$', program_views.ProgramFeaturedPageList.as_view()),
    re_path(r'^program/(?P<pk>[\d]+)/$', program_views.ProgramDetail.as_view()),
    #url(r'^api/program/$', cache_page(60 * 1440, key_prefix='program_list')(api_views.ProgramList.as_view()), name='program_list'),
    re_path(r'^program/$', program_views.ProgramList.as_view()),
    re_path(r'^topic/$', topic_views.TopicList.as_view()),
    re_path(r'^topic/(?P<pk>[\d]+)/$', topic_views.TopicDetail.as_view()),
    re_path(r'^subprogram/$', program_views.SubprogramList.as_view()),
    #url(r'^api/subprogram/(?P<pk>[\d]+)/$', cache_page(60 * 1440, key_prefix='subprogram_page')(api_views.SubprogramDetail.as_view()), name='subprogram'),
    re_path(r'^subprogram/(?P<pk>[\d]+)/$', program_views.SubprogramDetail.as_view()),
    re_path(r'^weekly/$', weekly_views.WeeklyList.as_view()),
    re_path(r'^weekly/(?P<pk>[\d]+)/$', weekly_views.WeeklyDetail.as_view()),
    re_path(r'^thread/$', thread_views.ThreadList.as_view()),
    re_path(r'^thread/detail/$', thread_views.TopLevelThreadDetail.as_view()),
    re_path(r'^thread/(?P<pk>[\d]+)/$', thread_views.ThreadDetail.as_view()),
    re_path(r'^report/(?P<pk>[\d]+)/$', report_views.ReportDetail.as_view()),
    re_path(r'^preview/$', meta_views.PreviewView.as_view()),
    re_path(r'^home/(?P<pk>[\d]+)/$', home_views.HomeDetail.as_view()),
    #url(r'^api/meta/$', cache_page(60 * 10080)(api_views.MetaList.as_view())),
    re_path(r'^meta/$', meta_views.MetaList.as_view()),
    #url(r'^api/content-types/$', cache_page(60 * 10080)(api_views.ContentList.as_view())),
    re_path(r'^content-types/$', meta_views.ContentList.as_view()),
    re_path(r'^subscribe/$', subscribe_views.subscribe),
    re_path(r'^jobs/$', jobs_views.JobsList.as_view()),
    re_path(r'^surveys-homepage/(?P<pk>[\d]+)/$', survey_views.SurveyHomeDetail.as_view()),
    re_path(r'^survey/(?P<pk>[\d]+)/$', survey_views.SurveyDetail.as_view())
]
