from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag
from mptt.forms import TreeNodeChoiceField

from .models import Screenshot, Category, Platform


class ScreenshotFilterForm(forms.Form):
    class SortChoices:
        BY_POPULARITY = '-when_created'
        BY_DATE = '-when_created'

        CHOICES = (
            (BY_POPULARITY, _('Popularity')),
            (BY_DATE, _('Date'))
        )

    """
    sort_by = forms.ChoiceField(
        choices=SortChoices.CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Sort by'),
        initial=SortChoices.BY_DATE
    )
    """

    def __init__(self, *args, **kwargs):
        app = kwargs.pop('app', '')
        self.screenshots = Screenshot.objects.all() if not app else app.screenshots.all()

        categories = Category.objects.filter(screenshots__in=self.screenshots).distinct()
        tags = Tag.objects.filter(screenshot__in=self.screenshots).distinct()
        #years = [[d.year, d.year] for d in self.screenshots.dates('when_created', 'year', order='DESC').distinct()]
        platforms = Platform.objects.filter(screenshots__in=self.screenshots).distinct()

        super().__init__(*args, **kwargs)

        self.fields['platforms'] = TreeNodeChoiceField(
            label=_('Platforms'),
            queryset=platforms,
            required=False,
            widget=forms.RadioSelect,
            level_indicator='---',
            empty_label=None
        )

        self.fields['categories'] = forms.ModelChoiceField(
            label=_('Categories'),
            queryset=categories,
            widget=forms.RadioSelect,
            required=False,
            empty_label=None
        )
        self.fields['tags'] = forms.ModelChoiceField(
            label=_('Tags'),
            queryset=tags,
            widget=forms.RadioSelect,
            required=False,
            empty_label=None
        )
        """
        self.fields['year'] = forms.ChoiceField(
            label=_('Year'),
            choices=years,
            required=False,
            widget=forms.RadioSelect
        )
        """
    def search(self):
        qs = self.screenshots
        if not self.is_valid():
            return qs

        if self.cleaned_data.get('categories', ''):
            qs = qs.filter(categories=self.cleaned_data['categories'])

        if self.cleaned_data.get('tags', ''):
            qs = qs.filter(tags=self.cleaned_data['tags'])

        if self.cleaned_data.get('platforms', ''):

            qs = qs.filter(platform__in=self.cleaned_data['platforms'].get_descendants(include_self=True))

        if self.cleaned_data.get('year', ''):
            qs = qs.filter(when_created__year=int(self.cleaned_data['year']))

        if self.cleaned_data.get('sort_by', ''):
            qs = qs.order_by(self.cleaned_data['sort_by'])

        return qs


class ScreenshotsAdminProcess(forms.Form):
    def validate_excel_file(value):
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.xlsx', '.xls']
        if not ext.lower() in valid_extensions:
            raise ValidationError(_('Unsupported file extension. Supports only .xls and .xlsx files'))

    excel_file = forms.FileField(validators=[validate_excel_file])