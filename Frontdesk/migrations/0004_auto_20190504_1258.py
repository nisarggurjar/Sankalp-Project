# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-04 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontdesk', '0003_auto_20190428_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='front_enquiry_data',
            name='follow_up_time',
            field=models.TimeField(max_length=100, null=True),
        ),
    ]