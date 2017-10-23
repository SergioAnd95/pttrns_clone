from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.models import Tag

from .models import Screenshot, Category


class ScreenshotFilterForm(forms.Form):
    class SortChoices:
        BY_POPULARITY = '-when_created'
        BY_DATE = '-when_created'

        CHOICES = (
            (BY_POPULARITY, _('Popularity')),
            (BY_DATE, _('Date'))
        )

    sort_by = forms.ChoiceField(
        choices=SortChoices.CHOICES,
        widget=forms.RadioSelect,
        required=False,
        label=_('Sort by'),
        initial=SortChoices.BY_DATE
    )

    def __init__(self, *args, **kwargs):
        app = kwargs.pop('app', '')
        self.screenshots = Screenshot.objects.all() if not app else app.screenshots.all()

        categories = Category.objects.filter(screenshots__in=self.screenshots).distinct()
        tags = Tag.objects.filter(screenshot__in=self.screenshots).distinct()

        super().__init__(*args, **kwargs)
        self.fields['categories'] = forms.ModelChoiceField(
            queryset=categories,
            widget=forms.RadioSelect,
            required=False,
            empty_label=None
        )
        self.fields['tags'] = forms.ModelChoiceField(
            queryset=tags,
            widget=forms.RadioSelect,
            required=False,
            empty_label=None
        )

    def search(self):
        qs = self.screenshots
        if not self.is_valid():
            return qs

        if 'categories' in self.cleaned_data:
            qs = qs.filter(categories=self.cleaned_data['categories'])

        if 'tags' in self.cleaned_data:
            qs = qs.filter(tags__id=self.cleaned_data['tags'])

        if self.cleaned_data.get('sort_by', ''):
            print(self.cleaned_data['sort_by'])
            qs = qs.order_by(self.cleaned_data['sort_by'])

        return qs
