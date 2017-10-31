from django.views.generic import FormView
from django.core.files import File
from django.utils.text import slugify
from django.shortcuts import render
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext_lazy as _

import requests
import io
import os
import itertools

import xlrd
from urllib import parse

from .forms import ScreenshotsAdminProcess
from .models import App, Screenshot, Category, Platform


def save_image_from_url(field, image_url):
    r = requests.get(image_url)

    if r.status_code == requests.codes.ok:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        print(r.content)
        img_filename = parse.urlsplit(image_url).path[1:]

        field.save(img_filename, File(img_temp), save=True)

        return True
    print(r.status_code)
    return False


class ProcessAppFormView(FormView):
    template_name = 'catalogue/admin/from_file_form.html'
    form_class = ScreenshotsAdminProcess
    success_url = '/admin/catalogue/app'
    categogry_cache = {}
    platform_cache = {}

    def form_valid(self, form):
        file = form.cleaned_data['excel_file']
        error_ctx = self.process_item(file)
        if error_ctx:
            return render(self.request, 'catalogue/admin/import_errors.html',
                          {'error': error_ctx, 'opts': App._meta})
        return super().form_valid(form)

    def get_app_images(self, sheet, start_pos):
        current_row = start_pos
        image_list = []
        while current_row < sheet.nrows:
            if not sheet.cell_value(current_row, 0) or current_row==start_pos:
                image_list.append({
                    'url': sheet.cell_value(current_row, 3),
                    'categories': sheet.cell_value(current_row, 4),
                    'tags': sheet.cell_value(current_row, 5),
                    'platform': sheet.cell_value(current_row, 6)
                })
            else:
                break
            current_row += 1

        return (current_row, image_list)

    def get_categories(self, *categories_names):
        categories = []
        for category_name in categories_names:
            if not category_name in self.categogry_cache:
                if Category.objects.filter(name=category_name).exists():
                    cat = Category.objects.get(name=category_name)
                else:
                    cat = Category.objects.create(
                        name=category_name,
                        slug=slugify(category_name)
                    )

                self.categogry_cache[category_name] = cat
            categories.append(self.categogry_cache[category_name])
        return categories

    def get_platform(self, platform_name):
        if not platform_name in self.platform_cache:
            if Platform.objects.filter(name=platform_name).exists():
                platform = Platform.objects.get(name=platform_name)
            else:
                platform = Platform.objects.create(
                    name=platform_name,
                    slug=slugify(platform_name)
                )

            return platform

        return self.platform_cache[platform_name]

    def process_item(self, file):
        workbook = xlrd.open_workbook(file_contents=file.read())
        first_sheet = workbook.sheet_by_index(0)
        erros = {}

        current_row = 1
        print(first_sheet.nrows)
        while current_row < first_sheet.nrows:
            app_name = first_sheet.cell_value(current_row, 0)

            if app_name and App.objects.filter(name=app_name).exists() or not app_name:
                current_row +=1
                continue

            next_row_pos, image_list = self.get_app_images(first_sheet, current_row)

            app = App.objects.create(
                name=app_name,
                slug=slugify(app_name),
                link=first_sheet.cell_value(current_row, 1)
            )
            save_image_from_url(app.logo, first_sheet.cell_value(current_row, 2))
            for img in image_list:
                screenshot = app.screenshots.create(
                    platform=self.get_platform(img['platform']),
                )
                screenshot.categories = self.get_categories(*img['categories'].split(', '))
                screenshot.tags.add(*img['tags'].split(', '))
                save_image_from_url(screenshot.image, img['url'])
                screenshot.save()
            current_row = next_row_pos

        """
         for row in itertools.islice(first_sheet.get_rows(), 1, None):
            app_name = row[0].value
            if not app_name.get
        """

        """
        for row in itertools.islice(first_sheet.get_rows(), 1, None):

            resource_name_en = row[3].value
            resource_name_ru = row[2].value if row[2].value else resource_name_en

            if not row[2].value:
                resource_name_ru = resource_name_en
            else:
                resource_name_ru = row[2].value

            if Resource.objects.filter(slug=slugify(resource_name_en)).exists():
                # if resource exists, skip other moves
                continue

            categories_names_ru = row[0].value.split(', ')
            categories_names_en = row[1].value.split(', ')
            categories_names = list(zip(categories_names_ru, categories_names_en))
            categories = []
            for category_name in categories_names:
                try:
                    category = Category.objects.get(name_ru=category_name[0])
                except:
                    category = Category.objects.create(
                        name_en=category_name[1],
                        name_ru=category_name[0],
                        slug=slugify(category_name[1])
                    )
                categories.append(category)
                try:
                    resource = Resource.objects.create(
                        name_en=resource_name_en,
                        name_ru=resource_name_ru,
                        slug=slugify(resource_name_en),
                        intro_text_ru=row[4].value,
                        intro_text_en=row[5].value,
                        full_text_ru=row[6].value,
                        full_text_en=row[7].value,
                        link=row[8].value,
                    )
                    resource.categories = categories
                    resource.tags.add(*row[9].value.split(', '))
                    resource.save()
                except Exception as e:
                    erros[resource_name_en] = e
        """
        return erros

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['opts'] = App._meta
        return ctx