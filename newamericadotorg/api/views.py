import django_filters, math
from django.db.models import Q
from django.utils.timezone import localtime, now

from rest_framework import status, pagination, mixins, generics, views, response, filters
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from django_filters.rest_framework import FilterSet

from wagtail.core.models import Page
from wagtail.search.models import Query

from home.models import Post, HomePage, OrgSimplePage
from person.models import Person

from .helpers import get_subpages
from newamericadotorg.settings.context_processors import content_types
from programs.models import Program, Subprogram, AbstractContentPage, AbstractProgram
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyArticle, WeeklyEdition
from report.models import Report
from other_content.models import OtherPost
from subscribe.campaign_monitor import update_subscriber
from ipware import get_client_ip
from newamericadotorg.api.expire_page_cache import expire_page_cache

from wagtail.search.backends import get_search_backend
