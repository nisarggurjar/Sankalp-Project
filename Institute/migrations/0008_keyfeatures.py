# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-06 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0007_auto_20190105_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('dis', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
