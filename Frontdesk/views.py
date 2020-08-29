from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import date,datetime,timedelta
import urllib
from Institute.views import *
from django.contrib.auth.models import User
from math import *
from Institute.models import *

def Institute_data(u  = None):
    if u:
        ins_data = Institite_profile.objects.filter(id = int(u.first_name)).first()
        return ins_data
    ins_data = Institite_profile.objects.filter().last()
    return ins_data

def Admin_data():
    admin_data = Admin_profile.objects.filter().first()
    return admin_data

def Running_batch_check(d, u):
    ins = Institite_profile.objects.filter(id = int(u.first_name)).first()
    running_batch = []
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    Tdate = int(''.join(date_reverse))

    if d == 0:
        all_batch = Master_batch_data.objects.filter(ins = ins)
    else:
        course = Master_course_data.objects.filter(id = d).first()
        all_batch = Master_batch_data.objects.filter(ins = ins, course = course)
    for batch in all_batch:
        ##### Start Date make As a Number #######

        startDate = batch.start_date
        d_split = startDate.split('/')
        d_reverse = d_split[3::-1]
        Sdate =  int(''.join(d_reverse))

        ##### End Date make As a Number #######

        EndDate = batch.end_date
        dd_split = EndDate.split('/')
        dd_reverse = dd_split[3::-1]
        Edate = int(''.join(dd_reverse))


        if Sdate<=Tdate and Edate>Tdate:
            running_batch.append(batch)
    return running_batch


def is_admin(user):
    if user.last_name == "Admin":
        return True
    return False

def is_Front_Officer(user):
    if user.last_name == "FrontDesk":
        return True
    return False

def is_Librarian(user):
    if user.last_name == "Library":
        return True
    return False

def is_Examinar(user):
    if user.last_name == "Exam":
        return True
    return False

def is_student(user):
    if user.last_name == "I_Student" or user.last_name == "E_Student":
        return True
    return False


def is_Institute_student(user):
    if user.last_name == "I_Student":
        return True
    return False

def is_External_student(user):
    if user.last_name == "E_Student":
        return True
    return False

#import urllib
#import urllib2
authkey = "232419AT2rwRRUo5b77e616"
def SendSMS(mobile, msg, sender):
    mobiles = mobile
    message = msg
    sender = sender
    route = "4"
    url = 'http://api.msg91.com/api/sendhttp.php'
    print("Hello")
    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route
    }
#    postdata = urllib.urlencode(values)  # URL encoding the data here.
 #   req = urllib2.Request(url, postdata)
  #  response = urllib2.urlopen(req)
   # output = response.read()


def home(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    total_income = 0
    upcoming_amount = 0
    todays_collection = 0
    previous_date = []
    sbc =0
    enq = 0
    cor_vise_t_add = []
    cor_vise_m_add = []
    cor_vise_t_enq = []
    cor_vise_m_enq = []
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    todays_followup =Todays_follow_up_date.objects.filter(ins = ins, fdate = today_date).count()

    all_students = Front_student_data.objects.filter(ins = ins,status = 'selected').count()
    d = Front_student_course_batch_data.objects.filter(ins = ins).order_by('-id')
    data = d[0:5]
    all_course = Master_course_data.objects.filter(ins = ins)
    all_enquiry = Front_enquiry_data.objects.filter(ins = ins)
    td = int(format_date[:2])
    for i in range(td-1,-1,-1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    for cour in all_course:
        course_filter = Master_course_data.objects.filter(id = cour.id).first()
        for prev in previous_date:
            sbc = sbc + Front_student_course_batch_data.objects.filter(ins = ins, course=course_filter,addmission_date = prev).count()
            enq = enq + Front_enquiry_data.objects.filter(ins = ins, course = course_filter,visited_date = prev).count()
        cor_vise_m_add.append(sbc)
        cor_vise_m_enq.append(enq)
        enq = 0
        sbc = 0
        sbc2 = Front_student_course_batch_data.objects.filter(ins = ins, course=course_filter,addmission_date = format_date).count()
        cor_vise_t_add.append(sbc2)
        enq2 = Front_enquiry_data.objects.filter(ins = ins, course = course_filter,visited_date = format_date).count()
        cor_vise_t_enq.append(enq2)


    for dd in d:
        total_income = total_income + int(dd.total_fee_pay)
        upcoming_amount = upcoming_amount + int(dd.fee_after_pay)

    for fee in Front_student_pay_fee.objects.filter(ins = ins):
        if fee.payment_date == format_date:
            todays_collection = todays_collection + int(fee.amount)

    rr = Running_batch_check(0, user)

    todays_enquiry = Front_enquiry_data.objects.filter(ins = ins, visited_date = format_date)
    todays_addmission = Front_student_course_batch_data.objects.filter(ins = ins, addmission_date = format_date)

    all_employe = Master_employee_data.objects.filter(ins = ins)

    context = {
        "all_students":all_students,"all_course":all_course,
        "all_enquiry":all_enquiry,"data":data,"total_income":total_income,
        "upcoming_amount":upcoming_amount,"todays_collection":todays_collection,
        "todays_enquiry":todays_enquiry.count(),"todays_addmission":todays_addmission.count(),
        "running_batch":len(rr),"todays_followup":todays_followup,"ma_list":cor_vise_m_add,
        "ta_list":cor_vise_t_add,"tanq_list":cor_vise_t_enq,"manq_list":cor_vise_m_enq,
        "all_employe":all_employe,"ins_data":Institute_data(user), "adminprofile":Admin_data()
        }

    return render(request,'front/front_deshboard.html',context)


#########Total Courses and Details ###########
def Front_Total_Courses(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    return render(request,'front/front_total_course.html',{"all_course":all_course,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def Front_Course_Details(request,course_id):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    course = Master_course_data.objects.filter(id = course_id).first()
    rr = Running_batch_check(course.id, user)


    return render(request,'front/front_course_details.html',{"course":course,"running_batch":len(rr),"ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Send_msg_for_new_addmission(sc, user):
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    setting_data = Auto_SMS_Settings_data.objects.filter().first()
    if setting_data:
        if setting_data.new_addmission:
            print("................................")
            sms = setting_data.sms_new_add.sms
            SplitSMS = sms.split("[[")
            final = SplitSMS[0]
            ns = format_date.split('/')
            ns = ns[3::-1]
            n11 = int(''.join(ns))
            ins_data = Institite_profile.objects.filter(id=int(user.first_name)).first()

            for i in range(1, len(SplitSMS)):
                print("Hello")
                msg = SplitSMS[i]
                z = msg.split("]]")

                w = z.pop(0)
                add = ''
                if w == "StudentName":
                    add = sc.student.name
                if w == "AdmissionDate":
                    add = sc.addmission_date
                if w == "RollNumber":
                    add = sc.student.roll_number
                if w == "Course":
                    add = sc.course.name
                if w == "FeesPackageAmount":
                    add = sc.course.master_fee_packege_data_set.first.total_fee
                if w == "TotalReceivedAmount":
                    add = sc.total_fee_pay
                if w == "TotalReceivableAmount":
                    add = sc.fee_after_pay
                if w == "InvoiceNo":
                    add = sc.front_student_pay_fee_set.last.invoice_number
                if w == "PaymentMode":
                    if sc.front_student_pay_fee_set.last.payment_mode_cheque:
                        add = sc.front_student_pay_fee_set.last.payment_mode_cheque
                    else:
                        add = sc.front_student_pay_fee_set.last.payment_mode_cash
                if w == "InstallmentDueDate" or "InstallmentAmount":
                    for ins in sc.front_student_fee_installment_data_set.all():
                        ns1 = ins.installment_last_date.split('/')
                        nsr = ns1[3::-1]
                        nsr = int(''.join(nsr))
                        if nsr >= n11:
                            aa = ins.installment_last_date
                            bb = ins.remaining_fee
                            break
                    if w == "InstallmentDueDate":
                        add = aa
                    if w == "InstallmentAmount":
                        add = bb

                if w == "BranchName":
                    add = ins_data.name
                if w == "BranchEmail":
                    add = ins_data.email

                if w == "BranchMobileNo":
                    add = ins_data.office_mob

                final += " " + add + " " + z[0]

            smsnum = ceil(len(final)/160)
            want_sms = smsnum * 1
            Now = NowSMS.objects.filter().first()
            ava = int(Now.num)
            if ava < want_sms:
                return redirect("Master:sms_fail")
            else:
                Now.num = ava-1
                Now.save()
            print("msg send")
            SendSMS(sc.student.mobile, final, setting_data.sms_new_add.sender_id)

from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.conf import settings
from django.template.loader import get_template, render_to_string
def Admission_Mail(email, institute, student, course, username, Pass ):
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    d = {
        'institute':institute,
        'student':student, 'course':course, 'username':username, 'pass':Pass
    }
    html = get_template("Inst/admission_mail.html").render(d)
    sub = institute.Title + " - New Admission"
    msg = EmailMultiAlternatives(sub, " ", from_email, to_email)
    msg.attach_alternative(html, "text/html")
    msg.send()



import random
################# Addmission######################
def Front_add_student(request,cor,bat,enquiry_id):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    Stu = NowStudents.objects.filter().first()
    n = int(Stu.num)
    if n <= 0:
        return redirect("Master:student_fail")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    form = Student_form()
    courseid = False
    data=False
    batch_data =False
    ins_ment_last_date = False
    all_course = Master_course_data.objects.filter(ins = ins)
    ins_list = []
    fee_type =[]
    admission_date = date.today()
    format_date = datetime.strptime(str(admission_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    enquiry_data = False

    Batch = []
    if cor != "0" and bat == "0":
        courseid = Master_course_data.objects.filter(id = cor).first()
        batches = Master_batch_data.objects.filter(ins = ins, course=courseid)
        Batch = []
        for b in batches:
            if b.master_installment_last_date_set.all():
                Batch.append(b)

    if cor !="0" and bat != "0":


        c = Master_course_data.objects.filter(id=cor).first()
        batch_data = Master_batch_data.objects.filter(id = bat).first()
        data = Master_fee_packege_data.objects.filter(ins = ins, course = c).first()

        if data:
            for i in data.master_make_installment_data_set.all():
                ins_list.append(int(i.percentage))

            for i in data.master_fee_type_packege_data_set.all():
                fee_type.append(int(i.fee))

        ins_ment_last_date = Master_installment_last_date.objects.filter(ins = ins, batch=batch_data)

        if request.method == "POST":

                form = Student_form(request.POST,request.FILES)
                print("Hello")

                if form.is_valid():
                    print("Hello")
                    instance = form.save()
                    if enquiry_id != "0":
                        enquiry_data = Front_enquiry_data.objects.filter(id=enquiry_id).first()
                        enquiry_data.status = 'close'
                        enquiry_data.save()
                    ###########Generate RollNumber ##########
                    dd = Institute_number.objects.get(ins = ins)
                    c_s_n = c.short_name
                    i_s_n = dd.ins_short_name
                    year = format_date[8:]
                    number = dd.number
                    dd.number = dd.number + 1
                    dd.save()
                    eighth_date = admission_date + timedelta(8)
                    if number < 10:
                        roll_number = c_s_n + i_s_n + year + '100' + str(number)
                    elif number >= 10 and number < 100:
                        roll_number = c_s_n + i_s_n + year + '10' + str(number)
                    elif number >= 100:
                        roll_number = c_s_n + i_s_n + year + '1' + str(number)
                    else:
                        pass


                    #########################################

                    instance.status = 'selected'
                    instance.roll_number = roll_number
                    instance.save()

                    # Create Student Account #####
                    uname = 0
                    while True:
                        name = instance.name
                        name = name.split()[0]
                        num = random.randint(100000, 999999)
                        uname = name + str(num)
                        usr = User.objects.filter(username = uname).first()
                        if not usr:
                            break
                    Pass = instance.mobile[:6]
                    user = User.objects.create_user(uname, instance.email, Pass)
                    user.last_name = "I_Student"
                    user.first_name = instance.name
                    user.save()

                    valid_day = request.POST['valid_day']
                    valid_date = admission_date + timedelta(int(valid_day))
                    id_card_vdate = datetime.strptime(str(valid_date), "%Y-%m-%d").strftime('%d/%m/%Y')
                    instance.id_card_validity = id_card_vdate
                    instance.usr = user
                    instance.ins = ins
                    instance.save()
                    dis_count = request.POST['dis_count']
                    course_total_fee = request.POST['course_total_fee']
                    student_data = Front_student_data.objects.filter(id=instance.id).first()
                    sc = Front_student_course_batch_data.objects.create(ins = ins, student =student_data,course = c,
                                                                   Batch = batch_data,addmission_date=format_date
                                                                        ,discount = dis_count,total_fee = course_total_fee,total_fee_pay = '0',
                                                                        fee_after_pay = course_total_fee
                                                                        ,course_cancel_date = eighth_date)
                    sc2 = Front_student_course_batch_data.objects.filter(id = sc.id).first()
                    for f in data.master_fee_type_packege_data_set.all():
                        nam = 'feeType' + str(f.id)
                        student_fee = request.POST[nam]

                        Front_student_fee_type_data.objects.create(ins = ins, student_course = sc2,name = f.fee_type,fee =student_fee )
                    aa = 0
                    last_date_list = []
                    for l in ins_ment_last_date:
                        last_date_list.append(l.last_date)
                    for inst in data.master_make_installment_data_set.all():
                        bb = last_date_list[aa]

                        nam2 = 'amount' + str(inst.id)

                        ins_amount = request.POST[nam2]

                        Front_student_fee_installment_data.objects.create(ins = ins, student_course=sc2, installment=inst.name, amount=ins_amount
                                                                          ,pay_fee = '0',remaining_fee = ins_amount,
                                                                          installment_last_date =bb )
                        aa = aa+1

                    Send_msg_for_new_addmission(sc, request.user)

                    Stu.num = int(Stu.num) - 1
                    Stu.save()
                    Admission_Mail(instance.email, Institute_data(request.user), instance.name, c.name, uname, Pass)

                    return redirect("Frontdesk:front_all_student")


    return render(request,'front/front_add_student.html',{"form":form,"courseid":courseid,"all_course":all_course,'batches':Batch,
                                                          "data":data,"ins_list":ins_list,"fee_type":fee_type
                                                          ,"batch_data":batch_data,"admission_date":format_date,
                                                          "enquiry_data":enquiry_data,"eid":enquiry_id,"ins_ment_last_date":ins_ment_last_date,
                                                          "ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Front_view_edit_student(request,option,sid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    student_data = Front_student_data.objects.filter(id = sid).first()


    if option == "View":
        button_show = True
        num = []
        li = []
        a = 0
        b = 0
        today_date = date.today()
        format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

        td = format_date.split('/')
        tds = td[3::-1]
        tdj = int(''.join(tds))
        tc = student_data.front_student_course_batch_data_set.count()

        for sc in student_data.front_student_course_batch_data_set.all():
            sad = sc.course_cancel_date.split('-')
            sadj = int(''.join(sad))
            if tdj<=sadj:
                li.append(sc)
            else:
                b = b+1


            for ftype in sc.front_student_fee_type_data_set.all():
                a = a + int(ftype.fee)
            num.append(a)
            a = 0
        if b == tc:
            button_show = False
        return render(request,'front/front_student_details.html',{"student_data":student_data,"total":num
                                                                  ,"li":li,"button_show":button_show,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

    if option == 'Edit':
        form = Student_form(instance=student_data)
        if request.method == "POST":


            return redirect('Frontdesk:front_VED_student' ,'View', student_data.id)

        return render(request, 'front/front_edit_student_details.html', {"student": student_data,"ins_data":Institute_data(user), "adminprofile":Admin_data(),"form":form})


def Front_AsignCourse_ToStudent(request,stu_id,cor,bat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = []
    course = Master_course_data.objects.filter(ins = ins)
    pack = []
    for p in course:
        d = p.master_fee_packege_data_set.all()
        if d:
            all_course.append(p)

    student_data = Front_student_data.objects.filter(id = stu_id).first()
    courseid = False
    batch = False
    ins_list = []
    fee_type = []
    Batch = []
    data = False
    error = False
    ins_ment_last_date = False
    admission_date = date.today()
    format_date = datetime.strptime(str(admission_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    if cor != '0':
        courseid = Master_course_data.objects.filter(id=cor).first()
        batches = Master_batch_data.objects.filter(ins = ins, course  = courseid)
        Batch = []
        for b in batches:
            if b.master_installment_last_date_set.all():
                Batch.append(b)
        ss = Front_student_course_batch_data.objects.filter(ins = ins, student = student_data,course = courseid).first()
        if ss:
            error = True

        data = Master_fee_packege_data.objects.filter(ins = ins, course=courseid).first()


        if data:
            for i in data.master_make_installment_data_set.all():
                ins_list.append(int(i.percentage))

            for i in data.master_fee_type_packege_data_set.all():
                fee_type.append(int(i.fee))

    if bat != '0':
        batch = Master_batch_data.objects.filter(id = bat).first()
        ins_ment_last_date = Master_installment_last_date.objects.filter(ins = ins, batch=batch)
        last_date_list = []
        for l in ins_ment_last_date:
            last_date_list.append(l.last_date)

        if request.method == "POST":
            dis_count = request.POST['dis_count']
            course_total_fee = request.POST['course_total_fee']
            eighth_date = admission_date + timedelta(8)
            sc = Front_student_course_batch_data.objects.create(ins = ins, student = student_data,course = courseid,
                                                                Batch = batch,addmission_date = format_date,
                                                                discount = dis_count,total_fee = course_total_fee,
                                                                total_fee_pay= '0',fee_after_pay = course_total_fee
                                                                , course_cancel_date=eighth_date)
            sc2 = Front_student_course_batch_data.objects.filter(id=sc.id).first()
            student_data.status = 'selected'
            student_data.save()
            for f in data.master_fee_type_packege_data_set.all():
                nam = 'feeType' + str(f.id)
                student_fee = request.POST[nam]

                Front_student_fee_type_data.objects.create(ins = ins, student_course=sc2, name=f.fee_type, fee=student_fee)
            a = 0
            print(last_date_list)
            for inst in data.master_make_installment_data_set.all():
                nam2 = 'amount' + str(inst.id)

                ins_amount = request.POST[nam2]

                Front_student_fee_installment_data.objects.create(ins = ins, student_course=sc2, installment=inst.name,
                                                                  amount=ins_amount, pay_fee='0',
                                                                  remaining_fee=ins_amount, installment_last_date = last_date_list[a])
                a = a+1
                Send_msg_for_new_addmission(sc, user)

            return redirect('Frontdesk:front_VED_student','View',stu_id)

    return render(request,'front/front_asign_course.html',{"student_id":stu_id,"courseid":courseid,"all_course":all_course, 'batches':Batch,
                                                           "batch":batch,"data":data,"ins_list":ins_list,"fee_type":fee_type
                                                           ,"ins_ment_last_date":ins_ment_last_date,"addmission_date":format_date,"error":error
                                                           ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Front_all_student(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_student = Front_student_data.objects.filter(ins = ins, status = 'selected')

    return render(request,'front/all_student.html',{"all_student":all_student,"ins_data":Institute_data(user), "adminprofile":Admin_data()})


############ Enquiry #################

def Front_enquiry(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    form = Enquiry_form()
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_courses = Master_course_data.objects.filter(ins = ins)
    all_enquiry = Front_enquiry_data.objects.filter(ins = ins)
    open_enquiry = Front_enquiry_data.objects.filter(ins = ins, status = 'open')
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    if request.method == "POST":

        form = Enquiry_form(request.POST)
        cid= request.POST['cid']
        tt = request.POST['time']
        cors = Master_course_data.objects.filter(id = cid).first()
        if form.is_valid():
            print("hello")
            instance = form.save(commit=False)
            instance.visited_date = format_date
            instance.status = 'open'
            instance.course = cors
            instance.ins = ins
            instance.follow_up_time = tt
            instance.save()
            next = instance.follow_up_date
            x = next.split('/')
            if len(x[0]) < 2:
                y = x.pop(0)
                y = '0' + y
                x.insert(0, y)

            if len(x[1]) < 2:
                y = x.pop(1)
                y = '0' + y
                x.insert(1, y)
            x = '/'.join(x)
            instance.save()
            return redirect('Frontdesk:front_enquiry')
        else:
            form = Enquiry_form()

    return render(request,'front/front_enquiry.html',{"form":form,"all_enquiry":all_enquiry
                                                      ,"visited_date":format_date,"open_enquiry":open_enquiry
                                                    ,"ins_data":Institute_data(user), "adminprofile":Admin_data(),

                                                      "all_courses":all_courses})
import csv
import openpyxl
def Front_Import_Enquiry(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Wrong_entry.csv"'
    writer = csv.writer(response)
    user = request.user
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()

    if request.method == "POST":
        file = request.FILES['csv']
        print(file.name)
        sheet = request.POST['sheet']
        wb = openpyxl.load_workbook(file, keep_vba=True)
        worksheet = wb[sheet]
        nn = 0
        for row in worksheet.iter_rows():
            n = 0
            main_data = []
            wrong_data = []
            for ceil in row:
                if ceil.value != None:
                    main_data.append(ceil.value)
                wrong_data.append(ceil.value)

            data = list(main_data)
            if len(data)== 4:
                Front_enquiry_data.objects.create(course_name =data[0],student_name=data[1],
                                                  mobile = data[2],email=data[3]
                                                  ,status= 'open',ins=ins)
            else:
                y = wrong_data.count(None)
                for i in range(y):
                    z = wrong_data.index(None)
                    wrong_data[z] = " "
                writer.writerow(wrong_data)
                nn += 1
        if nn>0:
            return response

        return redirect('Frontdesk:front_enquiry')




def Front_close_or_update_enquiry(request,eid,option):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_enquiry_data.objects.filter(id=eid).first()
    if option == "Update":
        dd = date.today()
        Todays_follow_up_date.objects.create(ins = ins, fdate=dd)
        format_date = datetime.strptime(str(dd), "%Y-%m-%d").strftime('%d/%m/%Y')

        if request.method == "POST":
            d = request.POST
            fdate = d['fdate']
            ftime = d['ftime']
            remark = d['remark']
            data.follow_up_time = ftime
            x = fdate.split('/')
            if len(x[0]) < 2:
                y = x.pop(0)
                y = '0' + y
                x.insert(0, y)
            if len(x[1]) < 2:
                y = x.pop(1)
                y = '0' + y
                x.insert(1, y)
            x = '/'.join(x)

            data.follow_up_date = x
            data.remark = remark
            data.todays_follow_up_date = format_date
            data.save()

    if option == "Close":
        data.status = 'close'
        data.save()

    return redirect(request.META.get('HTTP_REFERER'))


def Front_enquiry_followup_reminder(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    open_enquiry = Front_enquiry_data.objects.filter(ins = ins, status = 'open')
    today_date = date.today()
    li = []
    li2 = []
    for i in range(0, 6):
        tomorrow = today_date +timedelta(i)
        tomorrow1 = datetime.strptime(str(tomorrow), "%Y-%m-%d").strftime('%d/%m/%Y')
        d = tomorrow1.split('/')
        d = d[3::-1]
        d = int(''.join(d))
        li2.append(d)

    for fdate in open_enquiry:
        follow_date = fdate.follow_up_date
        follow_date_split = follow_date.split('/')

        follow_date_reverse = follow_date_split[3::-1]
        number2 = int(''.join(follow_date_reverse))
        for next_date in li2:

            if number2 == next_date:

                li.append(fdate)

    return render(request,'front/front_followup_reminder.html',{"open_enquiry":open_enquiry,"latest_followup_date":li,
                                                                "number":len(li),"ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Front_previous_follow_up(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    open_enquiry = Front_enquiry_data.objects.filter(ins = ins, status='open')
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    number1 = int(''.join(date_reverse))
    li = []

    for fdate in open_enquiry:
        follow_date = fdate.follow_up_date
        follow_date_split = follow_date.split('/')

        follow_date_reverse = follow_date_split[3::-1]
        number2 = int(''.join(follow_date_reverse))

        if number2 < number1:
            li.append(fdate)


    return render(request, 'front/front_previous_followup.html',
                  {"open_enquiry": open_enquiry, "latest_followup_date": li,
                   "number":len(li),"ins_data":Institute_data(user), "adminprofile":Admin_data()})


############## pay fee ############

def Front_student_collect_fee(request,cor,bat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    ins_data = Institute_data(user)
    all_course = Master_course_data.objects.filter(ins = ins)
    student_data = False
    batch = False
    course = False
    today_date = date.today()
    payment_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    if cor != '0' and bat == '0':
        course = Master_course_data.objects.filter(id = cor).first()
    if cor != '0' and bat != '0':
        batch = Master_batch_data.objects.filter(id = bat).first()
        student_data = batch.front_student_course_batch_data_set.all()

        if request.method == "POST":
            d = request.POST
            student_id = d['studnt_id']
            data = Front_student_data.objects.filter(id = student_id).first()
            student_course = Front_student_course_batch_data.objects.filter(ins = ins, Batch =batch,student = data ).first()
            mode = d['mode']
            amount = d['amount']
            total_amm = int(student_course.total_fee) - int(student_course.total_fee_pay)
            student_course.total_fee_pay = int(student_course.total_fee_pay) + int(amount)
            student_course.fee_after_pay = int(student_course.fee_after_pay) - int(amount)
            student_course.save()
            student_installment = student_course.front_student_fee_installment_data_set.all()
            am = amount


            for i in student_installment:
                if float(i.remaining_fee)> 0:

                    ff = float(i.remaining_fee) - float(am)
                    if ff<0:

                        i.pay_fee = float(i.pay_fee) + float(i.remaining_fee)
                        i.remaining_fee = 0
                        i.save()
                        am = abs(ff)

                    elif ff>0:
                        i.remaining_fee = ff
                        i.pay_fee = float(i.pay_fee)+float(am)
                        i.save()
                        break


                    else:
                        i.pay_fee = float(i.pay_fee) + float(i.remaining_fee)
                        i.remaining_fee = 0
                        i.save()
                        break



            if mode == 'cheque':
                bank_name = d['bank_name']
                ch_number = d['ch_number']
                ch_date = d['ch_date']

                data = Front_student_pay_fee.objects.create(ins = ins,  student_course =student_course,payment_mode_cheque = mode,
                                                     amount = amount,cheque_number =ch_number,Bank_name =  bank_name,
                                                     cheque_date = ch_date,payment_date =payment_date,
                                                     remain_ammount =student_course.fee_after_pay,total_amount = total_amm )

            else:
                data = Front_student_pay_fee.objects.create(ins = ins, student_course=student_course, payment_mode_cash=mode,
                                                     amount=amount,payment_date=payment_date,
                                                     remain_ammount=student_course.fee_after_pay, total_amount=total_amm)

            inv = Invoice_number_generate.objects.get(ins = ins)
            inv_number = inv.number
            inv.number = inv.number + 1
            inv.save()
            nn = inv.start_char + str(inv_number)
            data.invoice_number = nn
            data.save()
            data22 = Institite_profile.objects.filter().first()

            setting_data = Auto_SMS_Settings_data.objects.filter().first()
            if setting_data:
                if setting_data.student_fees:
                    sms = setting_data.sms_student_fee.sms
                    SplitSMS = sms.split("[[")
                    final = SplitSMS[0]
                    ns = payment_date.split('/')
                    ns = ns[3::-1]
                    n11 = int(''.join(ns))

                    for i in range(1, len(SplitSMS)):
                        print("Hello")
                        msg = SplitSMS[i]
                        z = msg.split("]]")

                        w = z.pop(0)
                        add = ''
                        if w == "StudentName":
                            add = student_course.student.name
                        if w == "AdmissionDate":
                            add = student_course.addmission_date
                        if w == "RollNumber":
                            add = student_course.student.roll_number
                        if w == "Course":
                            add = student_course.course.name
                        if w == "FeesPackageAmount":
                            add = student_course.course.master_fee_packege_data_set.first.total_fee
                        if w == "TotalReceivedAmount":
                            add = student_course.total_fee_pay
                        if w == "TotalReceivableAmount":
                            add = student_course.fee_after_pay
                        if w == "InvoiceNo":
                            add = student_course.front_student_pay_fee_set.last.invoice_number
                        if w == "PaymentMode":
                            if student_course.front_student_pay_fee_set.last.payment_mode_cheque:
                                add = student_course.front_student_pay_fee_set.last.payment_mode_cheque
                            else:
                                add = student_course.front_student_pay_fee_set.last.payment_mode_cash
                        if w == "InstallmentDueDate" or "InstallmentAmount":
                            for ins in student_course.front_student_fee_installment_data_set.all():
                                ns1 = ins.installment_last_date.split('/')
                                nsr = ns1[3::-1]
                                nsr = int(''.join(nsr))
                                if nsr >= n11:
                                    aa = ins.installment_last_date
                                    bb = ins.remaining_fee
                                    break
                            if w == "InstallmentDueDate":
                                add = aa
                            if w == "InstallmentAmount":
                                add = bb


                        if w == "BranchName":
                            add = ins_data.name
                        if w == "BranchEmail":
                            add = ins_data.email

                        if w == "BranchMobileNo":
                            add = ins_data.office_mob

                        final += " " + add + " " + z[0]

                    smsnum = ceil(len(final) / 160)
                    want_sms = smsnum * 1
                    Now = NowSMS.objects.filter().first()
                    ava = int(Now.num)
                    if ava < want_sms:
                        return redirect("Master:sms_fail")
                    else:
                        Now.num = ava - 1
                        Now.save()
                        SendSMS(student_course.student.mobile, final, setting_data.sms_student_fee.sender_id)

            return render(request, 'front/front_generate_invoice.html',{"data":data,"data22":data22})

    return render(request,'front/front_collect_fee.html',{"student_data":student_data,
                                                          "all_course":all_course,"course":course,"batch":batch
                                                          ,"payment_date":payment_date,"ins_data":ins_data,"adminprofile":Admin_data()})

def Front_generate_invoice(request,pid):
    print("hello python")
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    data = Front_student_pay_fee.objects.filter(id = pid).first()
    data22 = Institite_profile.objects.filter().first()
    print("hello python")
    return render(request,'front/front_generate_invoice.html',{"data":data,"data22":data22
                                                               ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def Front_fee_collection_reminder(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_batch = Master_batch_data.objects.filter(ins = ins)
    today_date = date.today()
    li = []
    li2 = []
    li3 = []
    li4 = []
    li5 = []

    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    number1 = int(''.join(date_reverse))
    for i in range(0, 6):
        tomorrow = today_date + timedelta(i)
        tomorrow1 = datetime.strptime(str(tomorrow), "%Y-%m-%d").strftime('%d/%m/%Y')
        d = tomorrow1.split('/')
        d = d[3::-1]
        d = int(''.join(d))
        li2.append(d)

    for batch in all_batch:
        for stu in batch.front_student_course_batch_data_set.all():
            a = 0
            b = 0
            if stu.fee_after_pay != '0':
                for ins in stu.front_student_fee_installment_data_set.all():
                    if ins.remaining_fee != '0':
                        ins_date_split = ins.installment_last_date.split('/')
                        ins_date_reverse = ins_date_split[3::-1]
                        number2 = int(''.join(ins_date_reverse))
                        if number2 < number1:
                            a = a + 1
                            li3.append(ins)
                            if a == 1:
                                li4.append(stu)


                        for next_date in li2:
                            if number2 == next_date:
                                b = b+1
                                li.append(ins)
                                if b == 1:
                                    li5.append(stu)

    return render(request,'front/front_fee_collection_reminder.html',{"li":li,"li3":li3,"li4":li4,"li5":li5,
                                                                      "ins_data": Institute_data(user),"adminprofile":Admin_data()})

def Front_Complete_FeePaidList(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    FeePaidList = Front_student_course_batch_data.objects.filter(ins = ins)
    return render(request,'front/complete_feepaid_list.html',{"FeePaidList":FeePaidList
                                                              ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})




########## Cancal Addmission #############

def Front_CancalAddmission(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if request.method == "POST":
        d = request.POST
        courseid = d['course']
        studentid = d['sid']
        cc = Master_course_data.objects.filter(id = courseid).first()
        ss = Front_student_data.objects.filter(id = studentid).first()
        data = Front_student_course_batch_data.objects.filter(ins = ins, student = ss,course = cc).first()
        batch = Master_batch_data.objects.filter(id = data.Batch.id).first()
        refund_money = data.total_fee_pay
        today_date = date.today()
        cancal_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

        Front_cancal_addmission_data.objects.create(ins = ins, student = ss,course = cc,batch = batch,refund_money = refund_money,cancal_date = cancal_date )
        if request.user.is_staff:
            data.delete()
        data1 = Front_student_course_batch_data.objects.filter(ins = ins, student=ss).first()
        if not data1:
            ss.status = 'cancal'
            ss.save()
            Stu = NowStudents.objects.filter().first()
            Stu.num = int(Stu.num) + 1
            Stu.save()

        return redirect('Frontdesk:front_VED_student','View',ss.id )



def Front_Cancal_AddmissionList(request,cor):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    course = False
    students = False
    if cor != '0':
        course = Master_course_data.objects.filter(id=cor).first()
        students = Front_cancal_addmission_data.objects.filter(ins = ins, course=course)

    context = {"course":course,"all_course":all_course,"students":students,"ins_data":Institute_data(user), "adminprofile":Admin_data()}

    return render(request,'front/front_cancal_addmission_list.html',context)


############# Filter Students ###########

def Front_filter_students(request,cor,bat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    students = False
    batch = False
    course = False
    if cor != '0':
        course = Master_course_data.objects.filter(id= cor).first()
        students = Front_student_course_batch_data.objects.filter(ins = ins, course = course)
    if bat != '0':
        batch = Master_batch_data.objects.filter(id = bat).first()
        students = Front_student_course_batch_data.objects.filter(ins = ins, course = course,Batch =batch )

    context = {"all_course":all_course,"students":students,"course":course,"batch":batch
               ,"ins_data":Institute_data(user), "adminprofile":Admin_data()}
    return render(request,'front/front_filter_students.html',context)


############### UPLOAD DOCUMENT Or Generate Id Card ############
def Front_UploadDoc_or_GenerateIdCard(request,cor,opt):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    today_date = date.today()
    upload_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    upload = True
    li = []
    batchlist = []
    if opt == "Idcard":
        upload = False
    all_course = Master_course_data.objects.filter(ins = ins)
    course = False
    rr = False
    if cor != '0':
        course = Master_course_data.objects.filter(id = cor).first()
        rr = Running_batch_check(course.id, user)
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if request.method == "POST":
        option = request.POST['option']
        if option == 'batches':
            batch_list = request.POST.getlist('batch')

            for i in batch_list:
                batch_data = Master_batch_data.objects.filter(id = i).first()
                batchlist.append(batch_data)

                student_data1 = Front_student_course_batch_data.objects.filter(ins = ins, Batch = batch_data)

                for ss in student_data1:
                    li.append(ss)
                    if opt == 'Idcard':
                        continue
                    document_file = request.FILES['document']
                    doc_file_name = document_file.name
                    name = request.POST['name']
                    ss2 = Front_student_data.objects.filter(id = ss.student.id).first()
                    Front_document_files.objects.create(ins = ins, student = ss2,document_file = document_file,
                                                        doc_name =name,doc_file_name = doc_file_name,upload_date = upload_date)
            if opt == 'UploadDoc':
                for ii in batchlist:
                    Front_All_Uploaded_document.objects.create(ins = ins, batch=ii, doc_name=name, doc_file=document_file,
                                                               upload_date=upload_date)

                return redirect('Frontdesk:front_all_uploded')
        if option == 'allstudent':
            student_data = Front_student_data.objects.filter(ins = ins,status='selected')
            li = Front_student_course_batch_data.objects.filter(ins = ins)
            for ss in student_data:
                if opt == 'Idcard':
                    break
                document_file = request.FILES['document']
                doc_file_name = document_file.name
                name = request.POST['name']
                ss2 = Front_student_data.objects.filter(id=ss.id).first()
                Front_document_files.objects.create(ins = ins, student=ss2, document_file=document_file,
                                                    doc_name =name,upload_date = upload_date
                                                    ,doc_file_name = doc_file_name)

        if opt == 'Idcard':
            roll = []
            for jj in li:
                roll.append(jj.student.roll_number)
            Rnumber = '___'.join(roll)
            return render(request,'front/front_idcard_generate.html',{"li":li,"ins_data":Institute_data(user), "adminprofile":Admin_data(),"Rnumber":Rnumber})

    return render(request,'front/front_upload_documents.html',{"all_course":all_course,"course":course,"upload":upload,
                                                               'rr':rr,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def Front_single_student_doc_idcard(request,sid,op):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    st = Front_student_data.objects.filter(id=sid).first()
    today_date = date.today()
    upload_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if op == 'DOC':
        if request.method == "POST":
            doc = request.FILES['doc']
            doc_file_name = doc.name
            doc_name = request.POST['doc_name']
            Front_document_files.objects.create(ins = ins, student = st,document_file = doc,
                                                doc_name = doc_name,upload_date = upload_date
                                                ,doc_file_name = doc_file_name)
            return redirect('Frontdesk:front_VED_student', 'View',st.id)
    if op == 'ID':
        if request.method == "POST":
            cc = request.POST['course']
            course = Master_course_data.objects.filter(id = cc).first()
            li = Front_student_course_batch_data.objects.filter(ins = ins, student =st,course=course )
            roll = []
            for jj in li:
                roll.append(jj.student.roll_number)
            Rnumber = '___'.join(roll)
            return render(request, 'front/front_idcard_generate.html', {"li": li,"ins_data":Institute_data(user), "adminprofile":Admin_data(),"Rnumber":Rnumber})
        return render(request, 'front/front_idcard_generate.html',
                      { "ins_data": Institute_data(user), "adminprofile": Admin_data(),})


def All_Batch_uploaded_documents(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_document_files.objects.filter(ins = ins).order_by('-id')
    li = []
    li2 =[]
    for i in data:
        if not i.doc_file_name in li:
            li.append(i.doc_file_name)
            li2.append(i)



    return render(request,'front/front_all_uploaded_doclist.html',{"data":li2,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

########### Receipts ###############

def Front_all_receipts(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data =  Front_student_pay_fee.objects.filter(ins = ins).order_by('-id')

    return render(request,'front/front_all_receipts.html',{"data":data,"ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Front_staff_id_card(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    employe_data = Master_employee_data.objects.filter(ins = ins)
    cc = employe_data.count()
    li = []
    StaffId_Number = []
    if request.method == "POST":
        empid = request.POST.getlist('empid')
        for i in empid:
            dd = Master_employee_data.objects.filter(id = i).first()
            li.append(dd)
            StaffId_Number.append(dd.employee_id)
        Rnumber = '___'.join(StaffId_Number)
        return render(request,'front/front_staff_id_generate.html',{"li":li, 'emid':Rnumber, "ins_data":Institute_data(user), "adminprofile":Admin_data()})

    return render(request,'front/front_staff_idcard.html',{"data":employe_data,"cc":cc,"ins_data":Institute_data(user), "adminprofile":Admin_data()})


######################## Notification #################


def Send_Notification_student(temp,by,students,user):
    institute_data = Institite_profile.objects.filter(id=int(user.first_name)).first()
    today_date = date.today()
    send_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    ns = send_date.split('/')
    ns = ns[3::-1]
    n1 = int(''.join(ns))


    data1 = SMSTemplate.objects.filter(id=temp).first()
    sms = data1.sms
    SplitSMS = sms.split("[[")
    final = SplitSMS[0]
    n = 0
    for st in students:
        n = n + 1
        for i in range(1, len(SplitSMS)):
            print("Hello")
            msg = SplitSMS[i]
            z = msg.split("]]")

            w = z.pop(0)
            add = ''
            if w == "BranchName":
                add = institute_data.name
            if w == "BranchEmail":
                add = institute_data.email

            if w == "BranchMobileNo":
                add = institute_data.office_mob

            if w == "StudentName":
                add = st.student.name
            if w == "AdmissionDate":
                add = st.addmission_date
            if w == "RollNumber":
                add = st.student.roll_number
            if w == "Course":
                add = st.course.name
            if w == "FeesPackageAmount":
                add = st.course.master_fee_packege_data_set.first.total_fee
            if w == "TotalReceivedAmount":
                add = st.total_fee_pay
            if w == "TotalReceivableAmount":
                add = st.fee_after_pay
            if w == "InvoiceNo":
                add = st.front_student_pay_fee_set.last.invoice_number
            if w == "PaymentMode":
                if st.front_student_pay_fee_set.last.payment_mode_cheque:
                    add = st.front_student_pay_fee_set.last.payment_mode_cheque
                else:
                   add = st.front_student_pay_fee_set.last.payment_mode_cash
            if w == "InstallmentDueDate" or "InstallmentAmount":
                for ins in st.front_student_fee_installment_data_set.all():
                    ns1 = ins.installment_last_date.split('/')
                    nsr = ns1[3::-1]
                    nsr = int(''.join(nsr))
                    if nsr >= n1:
                        aa = ins.installment_last_date
                        bb = ins.remaining_fee
                        break
                if w == "InstallmentDueDate":
                    add = aa
                if w == "InstallmentAmount":
                    add = bb

            final += " " + add + " " + z[0]

        if by == 'sms':
            if n == 1:
                smsnum = ceil(len(final)/160)
                want_sms = smsnum * len(students)
                Now = NowSMS.objects.filter().first()
                ava = int(Now.num)
                print(ava)
                if ava < want_sms:
                    return False
                else:
                    Now.num = ava - want_sms
                    Now.save()
            SendSMS(st.student.mobile, final, data1.sender_id)
            final = SplitSMS[0]

        if by == 'panal':
            ss = Front_student_data.objects.filter(id=st.student.id).first()
            Notification_on_panel.objects.create(ins = institute_data, student=ss, info=final,noti_date = send_date)
            final = SplitSMS[0]
    return True


def Send_Notification_staff(temp,by,staff_data,user):
    institute_data = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data1 = SMSTemplate.objects.filter(id=temp).first()
    sms = data1.sms
    SplitSMS = sms.split("[[")
    final = SplitSMS[0]
    n = 0
    for st in staff_data:
        n = n+1
        for i in range(1, len(SplitSMS)):

            msg = SplitSMS[i]
            z = msg.split("]]")

            w = z.pop(0)
            add = ''
            if w == "staff_member_name":
                add = st.name
            if w == "DOJ":
                add = st.join_date
            if w == "Designation_Name":
                add = st.designation
            if w == "BranchName":
                add = institute_data.name
            if w == "BranchEmail":
                add = institute_data.email

            if w == "BranchMobileNo":
                add = institute_data.office_mob
            final += " " + add + " " + z[0]
        if by == 'sms':
            if n == 1:
                smsnum = ceil(len(final)/160)
                want_sms = smsnum * len(staff_data)
                Now = NowSMS.objects.filter().first()
                ava = int(Now.num)
                if ava < want_sms:
                    return False
                else:
                    Now.num = ava - want_sms
                    Now.save()
            SendSMS(st.mobile, final, data1.sender_id)
            final = SplitSMS[0]
    return True


def Notification_for_Batch(request, cour, batch):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    Sms_Templates = False
    course = False
    panel = True
    show = False
    Batch = False

    if cour != '0':
        course = Master_course_data.objects.filter(id=cour).first()
    if cour != '0' and batch != '0':
        Sms_Templates = SMSTemplate.objects.all()
        if not Sms_Templates:
            show = True
        Batch = Master_batch_data.objects.filter(id=batch).first()
        print(Batch)
        data = Front_student_course_batch_data.objects.filter(ins = ins,Batch=Batch)

        if request.method == "POST":
            d = request.POST
            temp = d['sms_select']
            by = d['by']
            dta = Send_Notification_student(temp,by,data,request.user)
            if not dta:
                return redirect("Master:sms_fail")

            return redirect("Frontdesk:notification_batch", '0', '0')

    return render(request, "front/Batch_notification.html", {"all_course":all_course,
                                                             "course":course,"batch":Batch,
                                                             'Sms_Templates':Sms_Templates,"ForBatch":True
                                                             ,"ins_data":Institute_data(user), "adminprofile":Admin_data(),"panel":panel
                                                             ,"show":show})



def Notification_for_allstudents_or_staff(request,option):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    show = False
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    Sms_Templates = SMSTemplate.objects.all()
    if not Sms_Templates:
        show = True
    panel = False
    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']

        if option == 'AllStaff':
            staff_data = Master_employee_data.objects.filter(ins = ins)
            dta = Send_Notification_staff(temp, by, staff_data,request.user)
            if not dta:
                return redirect("Master:sms_fail")

    return render(request,'front/Batch_notification.html',{"Sms_Templates":Sms_Templates,"ins_data":Institute_data(user),
                                                           "adminprofile":Admin_data(),
                                                           "panel":panel,"show":show,"ForBatch":False})


def Select_student_for_notifi(request,cour,batch):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    course = False
    Batch = False
    total = False
    all_course = Master_course_data.objects.filter(ins = ins)
    if cour != '0':
        course = Master_course_data.objects.filter(id = cour).first()
    if batch != '0':
        Batch = Master_batch_data.objects.filter(id = batch).first()
        total = Front_student_course_batch_data.objects.filter( ins = ins, Batch=Batch).count()
        if request.method == "POST":
            d = request.POST
            stuid = d.getlist('stuid')
            collection = '-'.join(stuid)

            return redirect("Frontdesk:notification_for_single",collection)

    return render(request, 'front/select_student.html', {"course":course,"all_course":all_course,
                                                                 "Batch":Batch,"total":total
                                                         ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})


def Notification_for_single_student(request,ndata):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    Sms_Templates = SMSTemplate.objects.all()

    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']
        li = ndata.split('-')
        for i in li:
            data = Front_student_course_batch_data.objects.filter(id = i)
            Send_Notification_student(temp, by, data,request.user)
        return redirect('Frontdesk:select_student','0','0')
    return render(request,'front/single_student_notification.html',{"Sms_Templates":Sms_Templates,"ins_data":Institute_data(user), "adminprofile":Admin_data()})



def Notification_for_single_staff(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    Sms_Templates = SMSTemplate.objects.all()
    all_staff = Master_employee_data.objects.filter(ins = ins)
    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']
        staff_id = d['staff_id']
        staff_data = Master_employee_data.objects.filter(id = staff_id)
        dta = Send_Notification_staff(temp, by, staff_data,request.user)
        if not dta:
            return redirect("Master:sms_fail")


    return render(request,'front/notification_for_staff.html',{"Sms_Templates":Sms_Templates,
                                                               "all_staff":all_staff,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def Select_enquiry_students(request,cor):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    students = False
    Course = False
    if cor != '0':
        Course = Master_course_data.objects.filter(id = cor).first()
        students = Front_enquiry_data.objects.filter(ins = ins, course = Course,status ='open')

        if request.method == "POST":
            d = request.POST
            stuid = d.getlist('stuid')
            collection = '-'.join(stuid)

            return redirect("Frontdesk:notification_enquiry_student",collection)

    return render(request,'front/select_enquiry_student.html',{"all_course":all_course,"Course":Course,"students":students
                                                               ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def Notification_Enquiry_students(request,enq_data):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")

    Sms_Templates = SMSTemplate.objects.all()
    institute_data = Institite_profile.objects.filter().first()

    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        li = enq_data.split('-')
        data1 = SMSTemplate.objects.filter(id=temp).first()
        sms = data1.sms
        n = 0
        for i in li:
            n = n+1
            data = Front_enquiry_data.objects.filter(id=i).first()

            SplitSMS = sms.split("[[")
            final = SplitSMS[0]

            for i in range(1, len(SplitSMS)):

                msg = SplitSMS[i]
                z = msg.split("]]")

                w = z.pop(0)
                add = ''
                if w == "StudentName":
                    add = data.student_name
                if w == "EnquiryDate":
                    add = data.visited_date

                if w == "Course":
                    add = data.course.name
                if w == "BranchName":
                    add = institute_data.name
                if w == "BranchEmail":
                    add = institute_data.email

                if w == "BranchMobileNo":
                    add = institute_data.office_mob
                final += " " + add + " " + z[0]

            if n == 1:
                smsnum = ceil(len(final)/160)
                want_sms = smsnum * len(li)
                Now = NowSMS.objects.filter().first()
                ava = int(Now.num)
                if ava < want_sms:
                    return redirect("Master:sms_fail")
                else:
                    Now.num = ava - want_sms
                    Now.save()

            SendSMS(data.mobile, final, data1.sender_id)


        return redirect('Frontdesk:select_enq_students', '0')

    return render(request,'front/notification_enquiry_student.html',{"Sms_Templates":Sms_Templates,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

################## Create Call Logs ###########

def Front_student_call_logs(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Front_Officer(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    today_date = date.today()
    form = Call_log_form()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    all_call = Front_call_logs.objects.filter(ins = ins).order_by('-id')
    if request.method == "POST":
        cid = request.POST['cid']
        tt = request.POST['time']
        cour = Master_course_data.objects.filter(id = cid).first()
        form = Call_log_form(request.POST)

        if form.is_valid():

            instance = form.save(commit=False)
            instance.call_date = format_date
            next = instance.next_follow_up_date
            instance.course = cour
            instance.ins = ins
            instance.follow_up_time = tt
            instance.save()
            x = next.split('/')
            if len(x[0]) < 2:
                y = x.pop(0)
                y = '0' + y
                x.insert(0, y)
            if len(x[1]) < 2:
                y = x.pop(1)
                y = '0' + y
                x.insert(1, y)
            x = '/'.join(x)
            instance.next_follow_up_date = x
            instance.save()
            return redirect('Frontdesk:call_logs')
        else:
            form = Call_log_form()
    return render(request,'front/create_call_logs.html',{"all_calls":all_call,"form":form,"call_date":format_date
                                                         ,"ins_data":Institute_data(user), "adminprofile":Admin_data()
                                                         ,"all_course":all_course})



