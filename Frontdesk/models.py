from django.db import models
from Institute.models import *
from django.forms import ModelForm

COLOR_CHOICES = (
    ('','Gender'),
    ('male','Male'),
    ('female', 'Female'),

)



class Front_student_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ##### Basic Details #######
    roll_number = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(null=True, blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    dob = models.CharField(max_length=10, null=True,blank=True)
    address = models.TextField(max_length=500, null=True,blank=True)
    mobile = models.CharField(max_length=13, null=True,blank=True)
    email = models.CharField(max_length=100, null=True,blank=True)
    college = models.CharField(max_length=100, null=True,blank=True)
    graduation = models.CharField(max_length=100, null=True,blank=True)
    stream = models.CharField(max_length=100, null=True,blank=True)
    gender = models.CharField(max_length=10,choices=COLOR_CHOICES,default='Gender')
    #### Parents Details #########
    Father_name = models.CharField(max_length=100, null=True,blank=True)
    father_mob = models.CharField(max_length=13, null=True,blank=True)
    Occupation = models.CharField(max_length=100, null=True,blank=True)
    father_add = models.CharField(max_length=200, null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True)
    id_card_validity = models.CharField(max_length=10,null=True,blank=True)



    def __str__(self):
        return self.name

class Front_cancal_addmission_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Front_student_data,models.CASCADE,null=True)
    course = models.ForeignKey(Master_course_data,models.CASCADE,null=True)
    batch = models.ForeignKey(Master_batch_data,models.CASCADE,null=True)
    refund_money = models.CharField(max_length=100,null=True,blank=True)
    cancal_date = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.student.name + ' course ' + self.course.name

class Front_student_course_batch_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    ##### Course Details ########
    student = models.ForeignKey(Front_student_data,models.CASCADE,null=True,blank=True)
    course = models.ForeignKey(Master_course_data, models.CASCADE, null=True,
                               default='', blank=True)
    Batch = models.ForeignKey(Master_batch_data, models.CASCADE, null=True, default='', blank=True)
    addmission_date = models.CharField(max_length=100, null=True, blank=True)
    total_fee_pay = models.CharField(max_length=100, null=True, blank=True)
    fee_after_pay = models.CharField(max_length=100, null=True, blank=True)
    ##### Fee Details #######
    discount = models.CharField(max_length=100, null=True, blank=True)
    total_fee = models.CharField(max_length=100, null=True, blank=True)
    course_cancel_date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.student.name + ' -course-- ' + self.course.name + '- batch-- ' + self.Batch.name


class Front_student_fee_type_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student_course = models.ForeignKey(Front_student_course_batch_data,models.CASCADE,null=True)
    name =  models.CharField(max_length=100,null=True)
    fee =  models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.student_course.student.name + '--' + self.name + '--' + self.fee

class Front_student_fee_installment_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student_course = models.ForeignKey(Front_student_course_batch_data,models.CASCADE,null=True)
    installment = models.CharField(max_length=100,null=True)
    amount = models.CharField(max_length=100,null=True)
    pay_fee = models.CharField(max_length=100,null=True)
    remaining_fee = models.CharField(max_length=100,null=True)
    installment_last_date = models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.student_course.student.name + ' ' + self.installment + ' amount ' + self.amount

class Front_student_pay_fee(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student_course = models.ForeignKey(Front_student_course_batch_data, models.CASCADE, null=True)
    payment_mode_cash = models.CharField(max_length=100,null=True,blank=True)
    amount = models.CharField(max_length=100,null=True,blank=True)
    payment_mode_cheque = models.CharField(max_length=100,null=True,blank=True)
    cheque_number =  models.CharField(max_length=100,null=True,blank=True)
    Bank_name = models.CharField(max_length=100, null=True,blank=True)
    cheque_date = models.CharField(max_length=100, null=True,blank=True)
    payment_date = models.CharField(max_length=100,null=True,blank=True)
    remain_ammount = models.CharField(max_length=100,null=True,blank=True)
    total_amount = models.CharField(max_length=100,null=True,blank=True)
    invoice_number = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.student_course.student.name + ' payment_date ' + self.payment_date



class Front_enquiry_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Master_course_data,models.CASCADE,null=True ,default='')
    student_name = models.CharField(max_length=100,null=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    college = models.CharField(max_length=100,null=True,blank=True)
    graduation = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=13,null=True)
    email = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=100,null=True)
    follow_up_date = models.CharField(max_length=10,null=True)
    follow_up_time = models.CharField(max_length=100, null=True)
    remark = models.CharField(max_length=500,null=True)
    visited_date = models.CharField(max_length=100,null=True,blank=True)
    todays_follow_up_date = models.CharField(max_length=100, null=True,blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.student_name

##########Invoice Number #############

class Invoice_number_generate(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    start_char = models.CharField(max_length=100,null=True,blank=True)
    number = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return 'number ' + str(self.number)


class Institute_number(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    ins_short_name = models.CharField(max_length=100,null=True,blank=True)
    number = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.ins_short_name + ' number ' + str(self.number)


class Front_document_files(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Front_student_data,models.CASCADE,null=True)
    doc_name = models.CharField(max_length=100,null=True)
    document_file = models.FileField(null=True)
    doc_file_name = models.CharField(max_length=100,null=True)
    upload_date = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.student.name

class Front_All_Uploaded_document(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    batch = models.ForeignKey(Master_batch_data,models.CASCADE,null=True)
    doc_name = models.CharField(max_length=100,null=True)
    doc_file = models.FileField(null=True)
    upload_date = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.batch.name


class Todays_follow_up_date(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    fdate = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.fdate


##################### NOTIFICATION ##########

class Notification_on_panel(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Front_student_data, on_delete=models.CASCADE)
    info = models.CharField(max_length=2000, null=True, blank=True)
    noti_date =models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.student.name


################# Call Logs ###############

class Front_call_logs(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Master_course_data,null=True, on_delete=models.CASCADE,default='')
    student_name = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=100,null=True,blank=True)
    call_date = models.CharField(max_length=100,null=True,blank=True)
    next_follow_up_date = models.CharField(max_length=10,null=True,blank=True)
    remark = models.CharField(max_length=100,null=True,blank=True)
    follow_up_time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.course.name + ' - ' + self.student_name






