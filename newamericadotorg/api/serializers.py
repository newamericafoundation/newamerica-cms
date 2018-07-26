from django.shortcuts import render
from django.template import loader
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer, SerializerMethodField

from wagtail.core.models import Page, ContentType
from wagtail.documents.models import Document
from home.models import Post, CustomImage, OrgSimplePage, PostAuthorRelationship
from programs.models import Program, Subprogram, Project, BlogProject, AbstractContentPage
from person.models import Person
from issue.models import IssueOrTopic
from event.models import Event
from weekly.models import WeeklyEdition, WeeklyArticle
from in_depth.models import InDepthProject, InDepthSection
from report.models import Report
from subscribe.models import SubscriptionSegment

from django.core.urlresolvers import reverse
from django.utils.text import slugify

from .helpers import get_program_content_types, generate_image_url, generate_image_rendition, get_subpages, get_content_type
import datetime
