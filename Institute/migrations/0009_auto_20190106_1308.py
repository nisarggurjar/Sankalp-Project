# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-06 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0008_keyfeatures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyfeatures',
            name='dis',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]