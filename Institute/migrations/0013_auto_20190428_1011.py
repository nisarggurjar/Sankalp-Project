# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-28 04:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0012_auto_20190428_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master_fee_type_data',
            name='ins',
        ),
        migrations.RemoveField(
            model_name='master_medium_data',
            name='ins',
        ),
    ]
