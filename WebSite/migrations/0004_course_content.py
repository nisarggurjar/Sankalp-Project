# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-30 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0003_auto_20190530_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course_content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
