# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-28 13:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Institute', '0013_auto_20190428_1011'),
        ('LibraryPanel', '0002_auto_20190105_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='latefine',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
        migrations.AddField(
            model_name='library_issue_book',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
        migrations.AddField(
            model_name='master_book_data',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
        migrations.AddField(
            model_name='master_catbook_data',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
        migrations.AddField(
            model_name='master_e_book',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
        migrations.AddField(
            model_name='master_subcatbook_data',
            name='ins',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Institite_profile'),
        ),
    ]
