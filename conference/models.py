import json

from django.db import models
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import localtime, now
from home.models import Post
from programs.models import Program, Subprogram
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page
