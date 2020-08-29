# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-04 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0005_sms_pack_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('institute', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
