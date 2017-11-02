from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel
# Create your models here.


class SiteMETA(SingletonModel):
    title = models.CharField(max_length=255, default='Title')
    description = models.CharField(max_length=500, default='Description')
    keywords = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meta', help_text=_('For social nerworks'))
    favico = models.ImageField(upload_to='favico', help_text=_('For favico'))
    author = models.CharField(max_length=100)

    def __str__(self):
        return u"Site meta"

    class Meta:
        verbose_name = "Site META tags"