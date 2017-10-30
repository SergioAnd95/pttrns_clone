import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey
from sorl.thumbnail import get_thumbnail
# Create your models here.


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=30, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Platform(MPTTModel):
    name = models.CharField(_('Name'), max_length=30, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Platform')
        verbose_name_plural = _('Platforms')


class App(models.Model):
    link = models.URLField(_('Link'))
    name = models.CharField(_('Name'), max_length=30)
    slug = models.SlugField(_('Slug'), unique=True)
    when_created = models.DateTimeField(_('When created'), auto_now_add=True)
    when_updated = models.DateTimeField(_('When updated'), auto_now=True, help_text=_('Important for meta tags(seo)'))
    logo = models.ImageField(_('Logo'), upload_to='apps')
    description = models.CharField(_('Description'), max_length=500, )

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return 'application', (self.slug,)

    class Meta:
        verbose_name = _('App')
        verbose_name_plural = _('Apps')


class Screenshot(models.Model):

    def get_upload_path(self, filename):
        return os.path.join("screenshots/", self.app.slug, filename)

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