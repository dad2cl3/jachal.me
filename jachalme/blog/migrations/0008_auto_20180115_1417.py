# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-15 14:17
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180115_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('post_heading', wagtail.wagtailcore.blocks.CharBlock(max_length=40)), ('section_heading', wagtail.wagtailcore.blocks.CharBlock(max_length=40)), ('header_image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('inline_image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()))),
        ),
    ]
