# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Retail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('description_en', models.CharField(blank=True, max_length=100, null=True)),
                ('description_zh_hans', models.CharField(blank=True, max_length=100, null=True)),
                ('description_zh_hant', models.CharField(blank=True, max_length=100, null=True)),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
