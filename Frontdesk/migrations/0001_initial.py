# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-01 05:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Institute', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Front_All_Uploaded_document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(max_length=100, null=True)),
                ('doc_file', models.FileField(null=True, upload_to='')),
                ('upload_date', models.CharField(max_length=100, null=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_batch_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_call_logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('call_date', models.CharField(blank=True, max_length=100, null=True)),
                ('next_follow_up_date', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('follow_up_time', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_cancal_addmission_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_money', models.CharField(blank=True, max_length=100, null=True)),
                ('cancal_date', models.CharField(blank=True, max_length=100, null=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_batch_data')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_document_files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(max_length=100, null=True)),
                ('document_file', models.FileField(null=True, upload_to='')),
                ('upload_date', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Front_enquiry_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100, null=True)),
                ('father_name', models.CharField(max_length=100, null=True)),
                ('college', models.CharField(max_length=100, null=True)),
                ('graduation', models.CharField(max_length=100, null=True)),
                ('mobile', models.CharField(max_length=13, null=True)),
                ('email', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('follow_up_date', models.CharField(max_length=10, null=True)),
                ('follow_up_time', models.CharField(max_length=100, null=True)),
                ('remark', models.CharField(max_length=500, null=True)),
                ('visited_date', models.CharField(blank=True, max_length=100, null=True)),
                ('todays_follow_up_date', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('course', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_student_course_batch_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addmission_date', models.CharField(blank=True, max_length=100, null=True)),
                ('total_fee_pay', models.CharField(blank=True, max_length=100, null=True)),
                ('fee_after_pay', models.CharField(blank=True, max_length=100, null=True)),
                ('discount', models.CharField(blank=True, max_length=100, null=True)),
                ('total_fee', models.CharField(blank=True, max_length=100, null=True)),
                ('course_cancel_date', models.CharField(blank=True, max_length=100, null=True)),
                ('Batch', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_batch_data')),
                ('course', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_student_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('mobile', models.CharField(blank=True, max_length=13, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('college', models.CharField(blank=True, max_length=100, null=True)),
                ('graduation', models.CharField(blank=True, max_length=100, null=True)),
                ('stream', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('', 'Gender'), ('male', 'Male'), ('female', 'Female')], default='Gender', max_length=10)),
                ('Father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_mob', models.CharField(blank=True, max_length=13, null=True)),
                ('Occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('father_add', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('id_card_validity', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Front_student_fee_installment_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment', models.CharField(max_length=100, null=True)),
                ('amount', models.CharField(max_length=100, null=True)),
                ('pay_fee', models.CharField(max_length=100, null=True)),
                ('remaining_fee', models.CharField(max_length=100, null=True)),
                ('installment_last_date', models.CharField(max_length=100, null=True)),
                ('student_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_course_batch_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_student_fee_type_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('fee', models.CharField(max_length=100, null=True)),
                ('student_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_course_batch_data')),
            ],
        ),
        migrations.CreateModel(
            name='Front_student_pay_fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_mode_cash', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_mode_cheque', models.CharField(blank=True, max_length=100, null=True)),
                ('cheque_number', models.CharField(blank=True, max_length=100, null=True)),
                ('Bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cheque_date', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_date', models.CharField(blank=True, max_length=100, null=True)),
                ('remain_ammount', models.CharField(blank=True, max_length=100, null=True)),
                ('total_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=100, null=True)),
                ('student_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_course_batch_data')),
            ],
        ),
        migrations.CreateModel(
            name='Institute_number',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ins_short_name', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_number_generate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_char', models.CharField(blank=True, max_length=100, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification_on_panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(blank=True, max_length=2000, null=True)),
                ('noti_date', models.CharField(blank=True, max_length=2000, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_data')),
            ],
        ),
        migrations.CreateModel(
            name='Todays_follow_up_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fdate', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='front_student_course_batch_data',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_data'),
        ),
        migrations.AddField(
            model_name='front_document_files',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_data'),
        ),
        migrations.AddField(
            model_name='front_cancal_addmission_data',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Frontdesk.Front_student_data'),
        ),
    ]
