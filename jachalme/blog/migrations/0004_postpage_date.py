# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-14 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180114_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpage',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
