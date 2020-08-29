# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-31 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0008_auto_20190531_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Director_Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
