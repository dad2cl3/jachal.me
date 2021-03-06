# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-17 14:17
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20180116_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField((('post_heading', wagtail.wagtailcore.blocks.CharBlock(max_length=40)), ('section_heading', wagtail.wagtailcore.blocks.CharBlock(max_length=40)), ('inline_image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('code', wagtail.wagtailcore.blocks.StructBlock((('language', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('arduino', 'Arduino'), ('bash', 'Shell'), ('c', 'C'), ('css', 'CSS'), ('django', 'Django'), ('docker', 'Docker'), ('javascript', 'JavaScript'), ('json', 'JSON'), ('md', 'Markdown'), ('nginx', 'Nginx'), ('plpgsql', 'Pl/pgSQL'), ('postgresql', 'PostgreSQL'), ('python', 'Python'), ('sql', 'SQL'), ('sqlite3', 'SQLite3'), ('yaml', 'YAML')])), ('style', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('syntax', 'default')])), ('code', wagtail.wagtailcore.blocks.TextBlock())))), ('video', wagtail.wagtailembeds.blocks.EmbedBlock()), ('url', wagtail.wagtailcore.blocks.URLBlock()))),
        ),
    ]
