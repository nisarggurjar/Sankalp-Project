# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-31 03:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebSite', '0005_course_content_sub_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('sub_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='WebSite.Sub_course')),
            ],
        ),
    ]
