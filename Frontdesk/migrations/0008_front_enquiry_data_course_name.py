# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-22 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontdesk', '0007_front_document_files_doc_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='front_enquiry_data',
            name='course_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
