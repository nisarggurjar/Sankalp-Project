# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-06 11:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Institute', '0009_auto_20190106_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='visiteduser',
            name='usr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]