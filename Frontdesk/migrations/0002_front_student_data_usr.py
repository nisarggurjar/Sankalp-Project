# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-02 06:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Frontdesk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='front_student_data',
            name='usr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]