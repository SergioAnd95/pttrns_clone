import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import get_thumbnail
# Create your models here.


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=30)
    slug = models.SlugField(_('Slug'))

    def __str__(self):
        return self.name


class Platform(MPTTModel):
    name = models.CharField(_('Name'), max_length=30)
    slug = models.SlugField(_('Slug'))
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    def __str__(self):
        return self.name


class App(models.Model):
    link = models.URLField(_('Link'))
    name = models.CharField(_('Name'), max_length=30)
    slug = models.SlugField(_('Slug'))
    when_created = models.DateTimeField(_('When created'), auto_now_add=True)
    logo = models.ImageField(_('Logo'), upload_to='apps')
    description = models.TextField(_('Description'), blank=True, null=True)

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'application', (self.slug,)


class Screenshot(models.Model):

    def get_upload_path(self, filename):
        return os.path.join("screenshots/", self.app.name, filename)

    image = models.ImageField(_('Image'), upload_to=get_upload_path)
    when_created = models.DateTimeField(_('When created'), auto_now_add=True)
    tags = TaggableManager(blank=True, related_name='screenshots')

    app = models.ForeignKey('App', related_name='screenshots')
    categories = models.ManyToManyField(
        'Category',
        verbose_name=_('Categories'),
        related_name='screenshots'
    )
    platform = models.ForeignKey('Platform', related_name='screenshots')

    def admin_image(self):
        img = get_thumbnail(self.image, '80x80', crop='center', quality=99)
        return '<img src="%s"/>' % img.url

    admin_image.allow_tags = True

    class Meta:
        verbose_name = _('Screenshot')
        verbose_name_plural = _('Screenshots')
        ordering = ('-when_created', )