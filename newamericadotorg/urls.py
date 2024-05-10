from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls
from wagtail.images.views.serve import ServeView
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

import newamericadotorg.redirects as redirects
import newamericadotorg.views
from newamericadotorg.api.urls import api_urls
from rss_feed.feeds import (
    AuthorFeed,
    ContentFeed,
    EventFeed,
    EventProgramFeed,
    GenericFeed,
    ProgramFeed,
    SubprogramFeed,
)
from search.views import search as search_view

urlpatterns = [
    re_path(r"^django-admin/", admin.site.urls),
    re_path(r"^admin/autocomplete/", include(autocomplete_admin_urls)),
    re_path(r"^admin/", include(wagtailadmin_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    re_path(r"^images/", include(wagtailimages_urls)),
    re_path(r"^search/$", search_view, name="search"),
    re_path(r"^h_preview/$", newamericadotorg.views.preview, name="headless_preview"),
    re_path(r"^feed/$", GenericFeed()),
    re_path(r"^feed/program/(?P<program>[a-zA-z\-]*)/$", ProgramFeed()),
    re_path(r"^feed/subprogram/(?P<subprogram>[a-zA-z\-]*)/$", SubprogramFeed()),
    re_path(r"^feed/author/(?P<author>[a-zA-z\-]*)/$", AuthorFeed()),
    re_path(r"^feed/event/(?P<tense>future|past)/$", EventFeed()),
    re_path(r"^feed/event/(?P<program>[a-zA-z\-]*)/$", EventProgramFeed()),
    re_path(
        r"^feed/event/(?P<program>[a-zA-z\-]*)/(?P<tense>future|past)/$",
        EventProgramFeed(),
    ),
    re_path(r"^feed/(?P<content_type>[a-zA-z]*)/$", ContentFeed()),
    re_path(r"^feed/(?P<content_type>[a-zA-z]*)/(?P<program>[a-zA-z\-]*)/$", ContentFeed()),
    re_path(r"^api/", include(api_urls)),
    re_path(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(action="redirect"),
        name="wagtailimages_serve",
    ),
    re_path(
        r"^international-security/future-property-rights/[^.]*$",
        redirects.future_property_rights,
    ),
    re_path(
        r"^international-security/planetary-politics/[^.]*$",
        redirects.planetary_politics,
    ),
    re_path(r"^international-security/[^.]*$", redirects.future_security),
    re_path(
        r"^education-policy/dual-language-learners/[^.]*$",
        redirects.dual_language_learners,
    ),
    re_path(r"^bretton-woods-ii/[^.]*$", redirects.digi),
    re_path(r"^digital-impact-governance-inititiative/[^.]*$", redirects.digi),
    re_path(r"^national-network/[^.]*$", redirects.local),
    re_path(
        r"^public-interest-technology/new-practice-lab/[^.]*$",
        redirects.new_practice_lab,
    ),
    re_path(r"^public-interest-technology/[^.]*$", redirects.pit),
    re_path(r"^future-property-rights/[^.]*$", redirects.flh),
    re_path(r"", include(wagtail_urls)),
]

if settings.DEBUG:
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
