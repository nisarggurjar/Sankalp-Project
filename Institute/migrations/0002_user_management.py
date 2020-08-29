# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-01 19:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Institute', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Management',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_employee_data')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]