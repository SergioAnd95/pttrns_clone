# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertising',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
