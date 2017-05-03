from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtailimages import urls as wagtailimages_urls


from search.views import search as search_view
from rss_feed.feeds import GenericFeed, ContentFeed, AuthorFeed, ProgramFeed, SubprogramFeed, EventFeed, EventProgramFeed


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

    url(r'', include(wagtail_urls)),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
