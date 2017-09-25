# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
        ('cms', '0006_auto_20170924_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(blank=True)),
                ('body_en', wagtail.wagtailcore.fields.RichTextField(blank=True, null=True)),
                ('body_zh_hans', wagtail.wagtailcore.fields.RichTextField(blank=True, null=True)),
                ('body_zh_hant', wagtail.wagtailcore.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
