from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls
from wagtail.images import urls as wagtailimages_urls
from wagtail.images.views.serve import ServeView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from newamericadotorg.api.urls import api_urls

from search.views import search as search_view
from rss_feed.feeds import GenericFeed, ContentFeed, AuthorFeed, ProgramFeed, SubprogramFeed, EventFeed, EventProgramFeed

import newamericadotorg.redirects as redirects
import newamericadotorg.views

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/autocomplete/', include(autocomplete_admin_urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^images/', include(wagtailimages_urls)),

    url(r'^search/$', search_view, name='search'),
    url(r'^h_preview/$', newamericadotorg.views.preview, name='headless_preview'),

    url(r'^feed/$', GenericFeed()),
    url(r'^feed/program/(?P<program>[a-zA-z\-]*)/$', ProgramFeed()),
    url(r'^feed/subprogram/(?P<subprogram>[a-zA-z\-]*)/$', SubprogramFeed()),
    url(r'^feed/author/(?P<author>[a-zA-z\-]*)/$', AuthorFeed()),
    url(r'^feed/event/(?P<tense>future|past)/$', EventFeed()),
    url(r'^feed/event/(?P<program>[a-zA-z\-]*)/$', EventProgramFeed()),
    url(r'^feed/event/(?P<program>[a-zA-z\-]*)/(?P<tense>future|past)/$', EventProgramFeed()),
    url(r'^feed/(?P<content_type>[a-zA-z]*)/$', ContentFeed()),
    url(r'^feed/(?P<content_type>[a-zA-z]*)/(?P<program>[a-zA-z\-]*)/$', ContentFeed()),

    url(r'^api/', include(api_urls)),

    url(r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$', ServeView.as_view(action='redirect'), name='wagtailimages_serve'),

    url(r'^international-security/future-property-rights/[^.]*$', redirects.future_property_rights),
    url(r'^education-policy/dual-language-learners/[^.]*$', redirects.dual_language_learners),
    url(r'^bretton-woods-ii/[^.]*$', redirects.digi),
    url(r'^digital-impact-governance-inititiative/[^.]*$', redirects.digi),
    url(r'^national-network/[^.]*$', redirects.local),
    url(r'^public-interest-technology/new-practice-lab/[^.]*$', redirects.new_practice_lab),
    url(r'^public-interest-technology/[^.]*$', redirects.pit),
    url(r'^future-property-rights/[^.]*$', redirects.flh),

    url(r'', include(wagtail_urls)),

]

if settings.DEBUG:

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
