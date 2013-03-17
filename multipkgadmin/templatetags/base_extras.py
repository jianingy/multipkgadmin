from django import template
from django.core.urlresolvers import reverse_lazy

register = template.Library()


@register.simple_tag
def active_by_name(request, name):
    if request.path.startswith(str(reverse_lazy(name))):
        return "active"
    return ""
