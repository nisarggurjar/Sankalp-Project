# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-01 04:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Auto_SMS_Settings_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_addmission', models.BooleanField(default=False)),
                ('student_fees', models.BooleanField(default=False)),
                ('fee_reminder', models.BooleanField(default=False)),
                ('student_bday', models.BooleanField(default=False)),
                ('emp_bday', models.BooleanField(default=False)),
                ('new_ts_asign', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Institite_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('institute_logo', models.FileField(blank=True, null=True, upload_to='')),
                ('institute_image', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('office_add', models.CharField(blank=True, max_length=200, null=True)),
                ('office_mob', models.CharField(blank=True, max_length=100, null=True)),
                ('landline_no', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('pan_number', models.CharField(blank=True, max_length=100, null=True)),
                ('created_date', models.CharField(blank=True, max_length=100, null=True)),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Master_batch_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('start_date', models.CharField(max_length=100, null=True)),
                ('end_date', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=100, null=True)),
                ('batch_shot_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_course_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=20, null=True)),
                ('medium', models.CharField(max_length=100, null=True)),
                ('short_name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_designation_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_employee_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('', 'Gender'), ('male', 'Male'), ('female', 'Female')], default='Gender', max_length=10)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('qualification', models.CharField(blank=True, max_length=100, null=True)),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('quali_year', models.CharField(blank=True, max_length=100, null=True)),
                ('exp_year', models.CharField(blank=True, max_length=100, null=True)),
                ('discription_exp', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.CharField(blank=True, max_length=100, null=True)),
                ('aadhar_card', models.IntegerField(blank=True, null=True)),
                ('join_date', models.DateField(blank=True, max_length=10, null=True)),
                ('office_in_time', models.TimeField(blank=True, max_length=13, null=True)),
                ('office_out_time', models.TimeField(blank=True, max_length=13, null=True)),
                ('resume', models.FileField(blank=True, null=True, upload_to='')),
                ('salary', models.CharField(blank=True, max_length=13, null=True)),
                ('created_date', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_fee_packege_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('discount_for_single', models.CharField(max_length=100, null=True)),
                ('total_fee', models.CharField(max_length=100, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='Master_fee_type_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_fee_type_packege_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_type', models.CharField(max_length=100, null=True)),
                ('fee', models.CharField(max_length=100, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_fee_packege_data')),
            ],
        ),
        migrations.CreateModel(
            name='Master_holiday_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('start_date', models.CharField(max_length=100, null=True)),
                ('end_date', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_installment_last_date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_date', models.CharField(max_length=100, null=True)),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_batch_data')),
            ],
        ),
        migrations.CreateModel(
            name='Master_make_installment_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('amount', models.CharField(max_length=100, null=True)),
                ('percentage', models.CharField(max_length=100, null=True)),
                ('packege', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_fee_packege_data')),
            ],
        ),
        migrations.CreateModel(
            name='Master_medium_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_paymentmode_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_Sender_ID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Master_subject_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created_date', models.CharField(max_length=20, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data')),
            ],
        ),
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('sms', models.CharField(blank=True, max_length=5000, null=True)),
                ('sender_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Institute.Master_Sender_ID')),
            ],
        ),
        migrations.AddField(
            model_name='master_installment_last_date',
            name='installment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_make_installment_data'),
        ),
        migrations.AddField(
            model_name='master_batch_data',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Institute.Master_course_data'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_emp_bday',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_emp_bday', to='Institute.SMSTemplate'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_fee_reminder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_fee_reminder', to='Institute.SMSTemplate'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_new_add',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_new_add', to='Institute.SMSTemplate'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_new_ts_asign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_new_ts_asign', to='Institute.SMSTemplate'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_student_bday',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_student_bday', to='Institute.SMSTemplate'),
        ),
        migrations.AddField(
            model_name='auto_sms_settings_data',
            name='sms_student_fee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_student_fee', to='Institute.SMSTemplate'),
        ),
    ]
