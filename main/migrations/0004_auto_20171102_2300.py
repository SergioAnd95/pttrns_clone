# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 23:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20171102_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitemeta',
            name='favico',
            field=models.ImageField(default='', help_text='For favico', upload_to='favico'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitemeta',
            name='image',
            field=models.ImageField(help_text='For social nerworks', upload_to='meta'),
        ),
    ]
