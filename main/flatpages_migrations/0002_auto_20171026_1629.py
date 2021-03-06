# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-26 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flatpage',
            name='content_en',
            field=models.TextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='flatpage',
            name='content_ru',
            field=models.TextField(blank=True, null=True, verbose_name='content'),
        ),
        migrations.AddField(
            model_name='flatpage',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='flatpage',
            name='title_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='title'),
        ),
    ]
