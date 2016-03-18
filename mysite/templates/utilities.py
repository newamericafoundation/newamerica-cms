from datetime import date
from django import template
from django.conf import settings

from programs.models import Program

register = template.Library()

@register.simple_tag()
def listify(i):
	return i + 3