from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailimages import urls as wagtailimages_urls
from wagtail.wagtailimages.views.serve import ServeView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from search.views import search as search_view
from rss_feed.feeds import GenericFeed, ContentFeed, AuthorFeed, ProgramFeed, SubprogramFeed, EventFeed, EventProgramFeed
from newamericadotorg.api import views as api_views

import report.utils.views as report_views
import programs.views as program_views

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^images/', include(wagtailimages_urls)),

    url(r'^search/$', search_view, name='search'),

    url(r'^feed/$', GenericFeed()),
    url(r'^feed/program/(?P<program>[a-zA-z\-]*)/$', ProgramFeed()),
    url(r'^feed/subprogram/(?P<subprogram>[a-zA-z\-]*)/$', SubprogramFeed()),
    url(r'^feed/author/(?P<author>[a-zA-z\-]*)/$', AuthorFeed()),
    url(r'^feed/event/(?P<tense>future|past)/$', EventFeed()),
    url(r'^feed/event/(?P<program>[a-zA-z\-]*)/$', EventProgramFeed()),
    url(r'^feed/event/(?P<program>[a-zA-z\-]*)/(?P<tense>future|past)/$', EventProgramFeed()),
    url(r'^feed/(?P<content_type>[a-zA-z]*)/$', ContentFeed()),
    url(r'^feed/(?P<content_type>[a-zA-z]*)/(?P<program>[a-zA-z\-]*)/$', ContentFeed()),

    url(r'^api/post/$', api_views.PostList.as_view(), name='post_list'),
    url(r'^api/search/$', api_views.SearchList.as_view()),
    url(r'^api/event/$', api_views.EventList.as_view()),
    #url(r'^api/author/$', cache_page(60 * 10, key_prefix='author_list')(api_views.AuthorList.as_view()), name='author_list'),
    url(r'^api/author/$', api_views.AuthorList.as_view()),
    #url(r'^api/fellow/$', cache_page(60 * 10, key_prefix='fellow_list')(api_views.FellowList.as_view())),
    url(r'^api/fellow/$', api_views.FellowList.as_view()),
    #url(r'^api/program/(?P<pk>[\d]+)/$', cache_page(60 * 1440, key_prefix='program_page')(api_views.ProgramDetail.as_view()), name='program'),
    url(r'^api/program/(?P<pk>[\d]+)/$', api_views.ProgramDetail.as_view()),
    #url(r'^api/program/$', cache_page(60 * 1440, key_prefix='program_list')(api_views.ProgramList.as_view()), name='program_list'),
    url(r'^api/program/$', api_views.ProgramList.as_view()),
    #url(r'^api/program/fellowships/$', cache_page(60 * 1440, key_prefix='fellowship_list')(api_views.FellowshipList.as_view())),
    url(r'^api/program/fellowships/$', api_views.FellowshipList.as_view()),
    url(r'^api/topic/$', api_views.TopicList.as_view()),
    url(r'^api/topic/(?P<pk>[\d]+)/$', api_views.TopicDetail.as_view()),
    url(r'^api/subprogram/$', api_views.SubprogramList.as_view()),
    #url(r'^api/subprogram/(?P<pk>[\d]+)/$', cache_page(60 * 1440, key_prefix='subprogram_page')(api_views.SubprogramDetail.as_view()), name='subprogram'),
    url(r'^api/subprogram/(?P<pk>[\d]+)/$', api_views.SubprogramDetail.as_view()),
    url(r'^api/weekly/$', cache_page(60 * 5040, key_prefix='weekly_articles')(api_views.WeeklyList.as_view()), name='weekly_list'),
    url(r'^api/weekly/(?P<pk>[\d]+)/$', cache_page(60 * 5040, key_prefix='weekly_page')(api_views.WeeklyDetail.as_view()), name='weekly'),
    url(r'^api/report/(?P<pk>[\d]+)/$', cache_page(1, key_prefix='report')(api_views.ReportDetail.as_view()), name='report'),
    url(r'^api/in-depth/$', api_views.InDepthProjectList.as_view()),
    url(r'^api/in-depth/(?P<pk>[\d]+)/$', api_views.InDepthProjectDetail.as_view()),
    url(r'^api/home/(?P<pk>[\d]+)/$', api_views.HomeDetail.as_view()),
    #url(r'^api/meta/$', cache_page(60 * 10080)(api_views.MetaList.as_view())),
    url(r'^api/meta/$', api_views.MetaList.as_view()),
    #url(r'^api/content-types/$', cache_page(60 * 10080)(api_views.ContentList.as_view())),
    url(r'^api/content-types/$', api_views.ContentList.as_view()),
    url(r'^api/subscribe/$', api_views.subscribe),
    url(r'^api/jobs/$', api_views.JobsList.as_view()),
    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(action='redirect'), name='wagtailimages_serve'),

    url(r'^(?P<program>[a-zA-z\-]*)/(?P<subprogram>[a-zA-z\-]*)/(our-people|events|projects|publications|topics|subscribe)/$', program_views.redirect_to_subprogram),
    url(r'^(?P<program>[a-zA-z\-]*)/(our-people|events|projects|about|publications|topics|subscribe)/$', program_views.redirect_to_program),
    # url(r'^(?P<program>[a-zA-z\-]*)/(?P<subprogram>[a-zA-z\-]*)/$', program_views.redirect_project_page),
    url(r'^(?P<program>[a-zA-z\-]*)/reports/(?P<report_name>[a-zA-Z0-9_\.\-]*)/pdf/$', report_views.pdf),
    url(r'^(?P<program>[a-zA-z\-]*)/reports/(?P<report_name>[a-zA-Z0-9_\.\-]*)/pdf/html/$', report_views.pdf_html),
    url(r'^(?P<program>[a-zA-z\-]*)/reports/(?P<report_name>[a-zA-Z0-9_\.\-]*)/(?P<report_section>[a-zA-Z0-9_\.\-]*)/$', report_views.redirect_report_section),
    url(r'^(?P<program>[a-zA-z\-]*)/(?P<subprogram>[a-zA-z\-]*)/reports/(?P<report_name>[a-zA-Z0-9_\.\-]*)/pdf/$', report_views.pdf),
    url(r'^(?P<program>[a-zA-z\-]*)/(?P<subprogram>[a-zA-z\-]*)/reports/(?P<report_name>[a-zA-Z0-9_\.\-]*)/(?P<report_section>[a-zA-Z0-9_\.\-]*)/$', report_views.redirect_report_section),

    url(r'', include(wagtail_urls)),

]

if settings.DEBUG:

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
