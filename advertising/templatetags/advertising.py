from django import template

from advertising.models import Advertising

register = template.Library()


@register.inclusion_tag('advertising/advertising.html')
def show_advertisings(position):
    ads = Advertising.objects.filter(position=position, active=True)
    return {'ads': ads}