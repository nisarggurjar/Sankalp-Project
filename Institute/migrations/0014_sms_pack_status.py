# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-28 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0013_auto_20190428_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms_pack',
            name='status',
            field=models.CharField(blank=True, default='Applied', max_length=200, null=True),
        ),
    ]