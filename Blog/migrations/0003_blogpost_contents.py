# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0002_auto_20160310_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='Contents',
            field=models.TextField(default='This is the default blog post '),
            preserve_default=False,
        ),
    ]
