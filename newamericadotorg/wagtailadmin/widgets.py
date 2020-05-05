from django.forms import widgets
from django.template import loader


class LocationWidget(widgets.TextInput):
    template_name = 'wagtailadmin/location.html'

    def render(self, name, value, attrs=None, renderer=None):
        context = {
            'value': value,
        }
        if attrs is not None:
            context.update(attrs)

        return loader.get_template(self.template_name).render(attrs)
