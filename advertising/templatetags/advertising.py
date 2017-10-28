from django import template

from advertising.models import Advertising

register = template.Library()


@register.inclusion_tag('')
def show_advertisings(position):
    adverts = Advertising.objects.filter(position=position)
    return {'adverts': adverts}