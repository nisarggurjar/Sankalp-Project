from django.db import models
from django.contrib.auth.models import User


class Institite_profile(models.Model):
    usr = models.ForeignKey(User,models.CASCADE,null=True,blank=True)
    Title = models.CharField(max_length=100,null=True,blank=True)
    sub_title = models.CharField(max_length=100,null=True,blank=True)
    institute_logo = models.FileField(null=True,blank=True)
    institute_image = models.FileField(null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    office_add = models.CharField(max_length=200,null=True,blank=True)
    office_mob = models.CharField(max_length=100,null=True,blank=True)
    landline_no = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    website = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    pan_number = models.CharField(max_length=100,null=True,blank=True)
    created_date = models.CharField(max_length=100,null=True,blank=True)
    map = models.TextField(null = True,blank=True)
    def __str__(self):
        return self.name



class Master_course_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=20, null=True)
    medium = models.CharField(max_length=100,null=True)
    short_name = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name + '/' + self.medium


class Master_batch_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    course = models.ForeignKey(Master_course_data, models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    start_date =models.CharField(max_length=100, null=True)
    end_date = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)
    batch_shot_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name + ' - '+ self.course.name + ' course '


class Master_fee_type_data(models.Model):
    name = models.CharField(max_length=100,null=True)
    created_date = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class Master_fee_packege_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    course = models.ForeignKey(Master_course_data,models.CASCADE,null=True)
    name = models.CharField(max_length=100, null=True)
    discount_for_single = models.CharField(max_length=100,null=True)
    total_fee = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Master_make_installment_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    packege = models.ForeignKey(Master_fee_packege_data, models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    amount = models.CharField(max_length=100,null=True)

    percentage = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.packege.name + '---' + self.name

class Master_installment_last_date(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    batch = models.ForeignKey(Master_batch_data, models.CASCADE, null=True)
    installment = models.ForeignKey(Master_make_installment_data, models.CASCADE, null=True)
    last_date = models.CharField(max_length = 100,null=True)

    def __str__(self):
        return self.installment.packege.name + '--'+ self.installment.name + '--' + self.last_date


class Master_fee_type_packege_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    course = models.ForeignKey(Master_fee_packege_data, models.CASCADE, null=True)

    fee_type = models.CharField(max_length=100, null=True)
    fee = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.course.name + '---' + self.fee_type


class Master_subject_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    course = models.ForeignKey(Master_course_data,models.CASCADE,null=True)
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=20, null=True)


    def __str__(self):
        return self.name + '-' + self.course.name + '/' + self.course.medium



class Master_medium_data(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=20, null=True)


    def __str__(self):
        return self.name



class Master_holiday_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=100, null=True)
    start_date =models.CharField(max_length=100, null=True)
    end_date = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Master_designation_data(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.name

COLOR_CHOICES = (
    ('','Gender'),
    ('male','Male'),
    ('female', 'Female'),

)
class Master_employee_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    image = models.FileField(null=True,blank=True)
    name = models.CharField(max_length=100, null=True,blank=True)
    employee_id = models.CharField(max_length=100, null=True,blank=True)
    email = models.CharField(max_length=100, null=True,blank=True)
    mobile = models.CharField(max_length=100, null=True,blank=True)
    gender = models.CharField(max_length=10, choices=COLOR_CHOICES, default='Gender',blank=True)

    designation = models.CharField(max_length=100, null=True,blank=True)
    qualification = models.CharField(max_length=100, null=True,blank=True)
    university = models.CharField(max_length=100, null=True,blank=True)
    quali_year = models.CharField(max_length=100, null=True,blank=True)
    exp_year = models.CharField(max_length=100, null=True,blank=True)
    discription_exp = models.CharField(max_length=200, null=True,blank=True)
    address = models.CharField(max_length=100, null=True,blank=True)
    dob = models.CharField(max_length=100, null=True,blank=True)
    aadhar_card = models.IntegerField( null=True,blank=True)
    join_date = models.CharField(max_length=10, null=True,blank=True)
    office_in_time = models.CharField(max_length=13, null=True,blank=True)
    office_out_time = models.CharField(max_length=13, null=True,blank=True)
    resume = models.FileField(null=True,blank=True)
    salary = models.CharField(max_length=13, null=True,blank=True)

    created_date = models.CharField(max_length=100, null=True,blank=True)



class Master_paymentmode_data(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100, null=True)


    def __str__(self):
        return self.name


class Master_Sender_ID(models.Model):
    name = models.CharField(max_length=100, null=True)
    created_date = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class SMSTemplate(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    sender_id = models.ForeignKey(Master_Sender_ID, on_delete=models.SET_NULL, null=True,default='')
    sms = models.CharField(max_length=5000, null=True, blank=True)

    def __str__(self):
        return self.title





class Admin_profile(models.Model):
    usr = models.ForeignKey(User, models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    dob = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(null=True,blank=True)


    def __str__(self):
        return self.name

################### Auto  SMS Setings ####################
class Auto_SMS_Settings_data(models.Model):
    new_addmission = models.BooleanField(default=False)
    sms_new_add = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_new_add',null=True, blank=True)
    student_fees = models.BooleanField(default=False)
    sms_student_fee = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_student_fee',null=True, blank=True)
    fee_reminder = models.BooleanField(default=False)
    sms_fee_reminder = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_fee_reminder',null=True, blank=True)
    student_bday = models.BooleanField(default=False)
    sms_student_bday = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_student_bday',null=True, blank=True)
    emp_bday = models.BooleanField(default=False)
    sms_emp_bday = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_emp_bday',null=True, blank=True)
    new_ts_asign = models.BooleanField(default=False)
    sms_new_ts_asign = models.ForeignKey(SMSTemplate, on_delete=models.SET_NULL, related_name='sms_new_ts_asign',null=True, blank=True)


class User_Management(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emp = models.ForeignKey(Master_employee_data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)


class SMS_Pack(models.Model):
    usr = models.ForeignKey(User, null=True)
    Number = models.CharField(max_length=100, null=True, blank=True)
    paid = models.CharField(max_length=100, null=True, blank=True)
    Date = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, default="Applied", null=True, blank=True)

    def __str__(self):
        return self.Number + "  ----  " + self.status


class NowSMS(models.Model):
    num = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.num

class VisitedUser(models.Model):
    usr = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    institute = models.CharField(max_length=100, null=True, blank=True)


class KeyFeatures(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    dis = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title



class Student_Pack(models.Model):
    usr = models.ForeignKey(User, null=True)
    Number = models.CharField(max_length=100, null=True, blank=True)
    paid = models.CharField(max_length=100, null=True, blank=True)
    Date = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, default="Applied", null=True, blank=True)

    def __str__(self):
        return self.Number + "  ----  " + self.status


class NowStudents(models.Model):
    num = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.num
