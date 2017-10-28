from django.db import models
from django.utils.translation import ugettext_lazy as _
from froala_editor.fields import FroalaField

# Create your models here.


class Advertising(models.Model):
    class PositionChoices:
        TOP_LEFT = 1
        TOP_RIGHT = 2
        BOTTOM_LEFT = 3
        BOTTOM_RIGHT = 4

        CHOICES = (
            (TOP_LEFT, _('top left')),
            (TOP_RIGHT, _('top right')),
            (BOTTOM_LEFT, _('bottom left')),
            (BOTTOM_RIGHT, _('bottom right'))
        )

    rank = models.PositiveIntegerField(_('Rank'))
    position = models.PositiveSmallIntegerField(_('Position in page'), choices=PositionChoices.CHOICES)
    title = models.CharField(_('Title'), max_length=100)
    when_created = models.DateTimeField(_('When created'),auto_now_add=True)
    when_updated = models.DateTimeField(_('When updated'), auto_now=True)
    content = FroalaField(_('Content'))
    active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name_plural = _('Advertising')
        verbose_name = _('Advertising')
        ordering = ('position', 'rank')