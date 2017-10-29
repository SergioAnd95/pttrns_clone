from django.db import models

from solo.models import SingletonModel
# Create your models here.


class SiteMETA(SingletonModel):
    title = models.CharField(max_length=255, default='Title')
    description = models.CharField(max_length=500, default='Description')
    keywords = models.CharField(max_length=500)
    image = models.ImageField(upload_to='meta')
    author = models.CharField(max_length=100)

    def __str__(self):
        return u"Site meta"

    class Meta:
        verbose_name = "Site META tags"