from django.shortcuts import get_object_or_404

from el_pagination.views import AjaxListView

from .models import Screenshot, App
from .forms import ScreenshotFilterForm


class AllScreenshotsView(AjaxListView):
    model = Screenshot
    template_name = 'index.html'
    page_template = 'catalogue/screenshot_list_page.html'
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

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.page_template]
        else:
            return super().get_template_names()


class AppScreenshotsView(AjaxListView):
    parent_model = App
    template_name = 'catalogue/application.html'
    page_template = 'catalogue/screenshot_list_page.html'
    context_object_name = 'screenshots'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.parent_model, slug=kwargs['slug'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.form = ScreenshotFilterForm(app=self.object)
        if self.request.GET:
            self.form = ScreenshotFilterForm(self.request.GET, app=self.object)

        return self.form.search()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['form'] = self.form
        ctx['app'] = self.object
        ctx['page_template'] = self.page_template
        return ctx

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.page_template]
        else:
            return super().get_template_names()