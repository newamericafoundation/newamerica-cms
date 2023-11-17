from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic.base import RedirectView
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
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/autocomplete/", include(autocomplete_admin_urls)),
    url(r"^admin/", include(wagtailadmin_urls)),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^images/", include(wagtailimages_urls)),
    url(r"^search/$", search_view, name="search"),
    url(r"^h_preview/$", newamericadotorg.views.preview, name="headless_preview"),
    url(r"^feed/$", GenericFeed()),
    url(r"^feed/program/(?P<program>[a-zA-z\-]*)/$", ProgramFeed()),
    url(r"^feed/subprogram/(?P<subprogram>[a-zA-z\-]*)/$", SubprogramFeed()),
    url(r"^feed/author/(?P<author>[a-zA-z\-]*)/$", AuthorFeed()),
    url(r"^feed/event/(?P<tense>future|past)/$", EventFeed()),
    url(r"^feed/event/(?P<program>[a-zA-z\-]*)/$", EventProgramFeed()),
    url(
        r"^feed/event/(?P<program>[a-zA-z\-]*)/(?P<tense>future|past)/$",
        EventProgramFeed(),
    ),
    url(r"^feed/(?P<content_type>[a-zA-z]*)/$", ContentFeed()),
    url(r"^feed/(?P<content_type>[a-zA-z]*)/(?P<program>[a-zA-z\-]*)/$", ContentFeed()),
    url(r"^api/", include(api_urls)),
    url(
        r"^images/([^/]*)/(\d*)/([^/]*)/[^/]*$",
        ServeView.as_view(action="redirect"),
        name="wagtailimages_serve",
    ),
    url(
        r"^international-security/future-property-rights/[^.]*$",
        redirects.future_property_rights,
    ),
    url(
        r"^international-security/planetary-politics/[^.]*$",
        redirects.planetary_politics,
    ),
    url(r"^international-security/[^.]*$", redirects.future_security),
    url(
        r"^education-policy/dual-language-learners/[^.]*$",
        redirects.dual_language_learners,
    ),
    url(r"^bretton-woods-ii/[^.]*$", redirects.digi),
    url(r"^digital-impact-governance-inititiative/[^.]*$", redirects.digi),
    url(r"^national-network/[^.]*$", redirects.local),
    url(
        r"^public-interest-technology/new-practice-lab/[^.]*$",
        redirects.new_practice_lab,
    ),
    url(r"^public-interest-technology/[^.]*$", redirects.pit),
    url(r"^future-property-rights/[^.]*$", redirects.flh),
    path(
        "education-policy/early-elementary-education-policy/<path:path>",
        RedirectView.as_view(url="/early-elementary-education-policy/%(path)s"),
    ),
    path(
        "education-policy/prek-12-education/<path:path>",
        RedirectView.as_view(url="/prek-12-education/%(path)s"),
    ),
    path(
        "education-policy/higher-education/<path:path>",
        RedirectView.as_view(url="/higher-education/%(path)s"),
    ),
    path(
        "education-policy/teaching-learning-tech/<path:path>",
        RedirectView.as_view(url="/teaching-learning-tech/%(path)s"),
    ),
    url(r"", include(wagtail_urls)),
]

if settings.DEBUG:
    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
