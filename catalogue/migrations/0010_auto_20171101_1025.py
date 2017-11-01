# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0009_auto_20171031_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='description_en',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='app',
            name='description_ru',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='app',
            name='logo',
            field=models.ImageField(upload_to='apps/', verbose_name='Logo'),
        ),
    ]
