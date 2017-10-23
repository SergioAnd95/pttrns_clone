from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Screenshot, App
from .forms import ScreenshotFilterForm


class AllScreenshotsView(ListView):
    model = Screenshot
    template_name = 'index.html'
    context_object_name = 'screenshots'

    def get_queryset(self):
        self.form = ScreenshotFilterForm()
        if self.request.GET:
            self.form = ScreenshotFilterForm(self.request.GET)

        return self.form.search()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.form
        return ctx


class AppScreenshotsView(DetailView):
    model = App
    template_name = 'catalogue/application.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ScreenshotFilterForm(app=self.object)
        if self.request.GET:
            form = ScreenshotFilterForm(self.request.GET, app=self.object)
        ctx['form'] = form
        ctx['screenshots'] = form.search()
        return ctx