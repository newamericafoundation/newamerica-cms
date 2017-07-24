from django.forms import widgets
from django.shortcuts import render
from django.template import loader

class LocationWidget(widgets.TextInput):
    template_name = 'wagtailadmin/location.html'

    def render(self, name, value, attrs=None):
        attrs['value'] = value;
        return loader.get_template(self.template_name).render(attrs)
