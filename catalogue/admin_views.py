from django.views.generic import FormView
from django.core.files.base import File, ContentFile
from django.utils.text import slugify
from django.shortcuts import render
from django.core.files.temp import NamedTemporaryFile

import requests

import xlrd
from urllib import parse

from .forms import ScreenshotsAdminProcess
from .models import App, Screenshot, Category, Platform


class ProcessAppFormView(FormView):
    template_name = 'catalogue/admin/from_file_form.html'
    form_class = ScreenshotsAdminProcess
    success_url = '/admin/catalogue/app'
    categogry_cache = {}
    platform_cache = {}
    errors = {}

    def form_valid(self, form):
        file = form.cleaned_data['excel_file']
        error_ctx = self.process_item(file)
        if error_ctx:
            return render(self.request, 'catalogue/admin/import_errors.html',
                          {'errors': error_ctx, 'opts': App._meta})
        return super().form_valid(form)

    def save_image_from_url(self, field, image_url, app_name):
        r = requests.get(image_url)

        if r.status_code == requests.codes.ok:
            img_temp = ContentFile(r.content)
            img_filename = parse.urlparse(image_url).path.split('/')[-1]

            try:
                field.save(img_filename, img_temp, save=True)
            except Exception as e:
                self.errors.update({app_name: '%s This is not image' % image_url})
                return False

            return True
        self.errors.update({app_name: 'URL:  not available' % image_url})
        return False

    def get_app_images(self, sheet, start_pos):
        current_row = start_pos
        image_list = []
        while current_row < sheet.nrows:
            if not sheet.cell_value(current_row, 0) or current_row == start_pos:
                image_list.append({
                    'url': sheet.cell_value(current_row, 7),
                    'categories': sheet.cell_value(current_row, 8),
                    'tags': sheet.cell_value(current_row, 9),
                    'platform': sheet.cell_value(current_row, 2)
                })
            else:
                break
            current_row += 1

        return (current_row, image_list)

    def get_categories(self, *categories_names):
        categories = []
        for category_name in categories_names:
            n = slugify(category_name)
            if not category_name in self.categogry_cache:
                if Category.objects.filter(slug__iexact=n).exists():
                    cat = Category.objects.get(slug__iexact=n)
                else:
                    cat = Category.objects.create(
                        name_en=category_name,
                        slug=slugify(category_name)
                    )

                self.categogry_cache[category_name] = cat
            categories.append(self.categogry_cache[category_name])
        return categories

    def get_platform(self, platform_name):
        if not platform_name in self.platform_cache:
            if Platform.objects.filter(name__iexact=platform_name).exists():
                platform = Platform.objects.get(name__iexact=platform_name)
            else:
                platform = Platform.objects.create(
                    name_en=platform_name,
                    slug=slugify(platform_name)
                )

            return platform

        return self.platform_cache[platform_name]

    def process_item(self, file):
        workbook = xlrd.open_workbook(file_contents=file.read())
        first_sheet = workbook.sheet_by_index(0)

        current_row = 1
        while current_row < first_sheet.nrows:
            app_name = first_sheet.cell_value(current_row, 0)

            if app_name and App.objects.filter(name_en=app_name).exists() or not app_name:
                current_row += 1
                continue

            next_row_pos, image_list = self.get_app_images(first_sheet, current_row)

            try:
                app = App.objects.create(
                    name_en=app_name,
                    name_ru=first_sheet.cell_value(current_row, 1),
                    slug=slugify(app_name),
                    link=first_sheet.cell_value(current_row, 3),
                    developer_name=first_sheet.cell_value(current_row, 5),
                    developer_link=first_sheet.cell_value(current_row, 6)
                )
            except Exception as e:
                self.errors.update({app_name: e})

            self.save_image_from_url(app.logo, first_sheet.cell_value(current_row, 4), app_name)
            for img in image_list:
                screenshot = app.screenshots.create(
                    platform=self.get_platform(img['platform']),
                )
                screenshot.categories = self.get_categories(*img['categories'].split(', '))
                screenshot.tags.add(*img['tags'].split(', '))
                self.save_image_from_url(screenshot.image, img['url'], app_name)
                screenshot.save()
            current_row = next_row_pos

        return self.errors

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['opts'] = App._meta
        return ctx