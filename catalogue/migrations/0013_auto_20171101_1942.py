# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0012_auto_20171101_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='developer_link',
            field=models.URLField(blank=True, null=True, verbose_name='Developer link'),
        ),
        migrations.AlterField(
            model_name='app',
            name='developer_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Developer name'),
        ),
    ]