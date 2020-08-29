from django.shortcuts import render, redirect
from .models import *
from datetime import date, datetime, timedelta
from LibraryPanel.models import *
from Frontdesk.models import *
from Frontdesk.views import *
import calendar
from ExamPanel.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from math import *

from instamojo_wrapper import Instamojo
import requests
import ast
import json




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

def is_website(user):
    if user.last_name == "yadav":
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


def Register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['username']
        institute = request.POST['pass']
        VisitedUser.objects.create(name=name, email=email, mobile=mobile,
                                   institute=institute)
        return redirect("login")
    return render(request, "Inst/register.html")


def ForgotPass(request):
    error = False
    valid = False
    who = ""
    email = ""
    username = ""
    perror = False
    if request.method == "POST":
        who = request.POST['who']
        email = request.POST['email']
        username = request.POST['username']
        ps = request.POST['ps1']
        ps1 = request.POST['ps2']
        usr = ""
        if who == "Admin":
            usr = User.objects.filter(username=username, email=email, last_name="Admin").first()
            if usr:
                valid = True
                error = False
            else:
                error = True

        if who == "FrontDesk":
            usr = User.objects.filter(username=username, email=email, last_name="FrontDesk").first()
            if usr:
                valid = True
                error = False
            else:
                error = True

        if who == "Library":
            usr = User.objects.filter(username=username, email=email, last_name="Library").first()
            if usr:
                valid = True
                error = False
            else:
                error = True
        if who == "Exam":
            usr = User.objects.filter(username=username, email=email, last_name="Exam").first()
            if usr:
                valid = True
                error = False
            else:
                error = True
        if who == "Student":
            usr = User.objects.filter(username=username, email=email, last_name="I_Student").first()
            if not usr:
                usr = User.objects.filter(username=username, email=email, last_name="E_Student").first()
            if usr:
                valid = True
                error = False
            else:
                error = True
        if usr and ps1 != '0' and ps != '0':
            if ps != ps1:
                perror = True
            else:
                usr.set_password(ps)
                usr.save()
                return redirect("login")
    context = {
        'error': error, 'valid': valid, 'who': who, 'email': email, 'username': username
    }

    return render(request, "Inst/forgot_pass.html", context)





def Login(request):
    if not request.user.is_authenticated():
        error = False
        if request.method == "POST":
            un = request.POST['username']
            Pass = request.POST['pass']
            user = authenticate(username=un, password=Pass)
            if user:
                login(request, user)
                return redirect("login")
            error = True
        return render(request, "Inst/login.html", {'error': error})
    user = request.user
    if is_admin(user):
        profile = user.institite_profile_set.first()
        if not profile:
            return redirect("Master:admin_institute_profile")
        if int(user.first_name) == 0:
            return redirect("Master:choose_institute")
        return redirect("Master:master_deshboard")
    elif is_Front_Officer(user):
        return redirect("Frontdesk:home")
    elif is_Examinar(user):
        return redirect("ExamPanel:exam_home")
    elif is_Librarian(user):
        return redirect("LibraryPanel:library_deshboard")
    elif is_student(user):
        return redirect("StudentPanel:home")
    elif is_website(user):
        return redirect("website_home")
    else:
        logout(request)
        return redirect("login")


def Admin_Choose_Institute(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    user = User.objects.filter(username = request.user.username).first()
    institutes = Institite_profile.objects.all()
    if request.method == "POST":
        i = request.POST["institute"]
        user.first_name = i
        user.save()
        return redirect("Master:master_deshboard")
    return render(request, "Inst/admin_choose_institute.html", {"institutes":institutes})




def Logout(request):
    user = request.user
    if is_admin(user):
        user.first_name = 0
        user.save()

    logout(request)
    return redirect("login")


def admin_show():
    admin = Admin_profile.objects.filter().first()
    return admin


def Total_Year_Sales(ins):
    Y = 0
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    dsplit = format_date.split('/')
    year = int(dsplit[2])
    for i in range(1, 13):
        a = calendar.monthrange(year, i)[1]
        days = [date(year, i, day) for day in range(1, a + 1)]
        for d in days:
            dd = datetime.strptime(str(d), "%Y-%m-%d").strftime('%d/%m/%Y')
            pyments = ExamInvoiceGenerate.objects.filter(date=dd)
            for p in pyments:
                Y = Y + int(p.paid_fee)
            ad_payments = Front_student_pay_fee.objects.filter(ins = ins, payment_date=dd)
            for ap in ad_payments:
                Y = Y + int(ap.amount)
    return Y


def Five_upcoming_follow_ups(user):
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    open_enquiry = Front_enquiry_data.objects.filter(ins = ins, status='open')
    today_date = date.today()
    li = []
    li2 = []
    for i in range(0, 6):
        tomorrow = today_date + timedelta(i)
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
    return li


def Master_Deshboard(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id = int(user.first_name)).first()

    addmission_sales = 0
    packege_sales = 0
    upcoming_amount = 0
    todays_collection = 0
    previous_date = []
    enq = 0
    cor_vise_t_enq = []
    cor_vise_m_enq = []
    li = []
    amount_this_month = []
    amount_overall = []
    today_amount = []
    am = 0
    am1 = 0
    am2 = 0

    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    todays_followup = Todays_follow_up_date.objects.filter(ins = ins, fdate=today_date).count()

    all_students = Front_student_data.objects.filter(ins = ins, status='selected').count()
    d = Front_student_course_batch_data.objects.filter(ins = ins).order_by('-id')
    data = d[0:5]
    all_course = Master_course_data.objects.filter(ins = ins)
    all_enquiry = Front_enquiry_data.objects.filter(ins = ins)
    td = int(format_date[:2])

    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)

    for cour in all_course:
        for st in cour.front_student_course_batch_data_set.all():
            all_payments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st)
            for allpay in all_payments:
                am2 = am2 + int(allpay.amount)

            tpayments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st, payment_date=format_date)
            for tpa in tpayments:
                am1 = am1 + int(tpa.amount)
            for pdate in previous_date:

                payments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st, payment_date=pdate)
                for pa in payments:
                    am = am + int(pa.amount)

        close = Front_enquiry_data.objects.filter(ins = ins, course=cour, status='close').count()
        li.append(close)
        amount_this_month.append(am)
        today_amount.append(am1)
        amount_overall.append(am2)
        am1 = 0
        am = 0
        am2 = 0
        for prev in previous_date:
            enq = enq + Front_call_logs.objects.filter(ins = ins, course=cour, call_date=prev).count()
        cor_vise_m_enq.append(enq)
        enq = 0
        enq2 = Front_call_logs.objects.filter(ins = ins, course=cour, call_date=format_date).count()
        cor_vise_t_enq.append(enq2)

    for pfee in ExamInvoiceGenerate.objects.all():
        packege_sales = packege_sales + int(pfee.paid_fee)
        upcoming_amount = upcoming_amount + int(pfee.remain_fee)

    for dd in d:
        addmission_sales = addmission_sales + int(dd.total_fee_pay)
        upcoming_amount = upcoming_amount + int(dd.fee_after_pay)

    for fee in Front_student_pay_fee.objects.filter(ins = ins):
        if fee.payment_date == format_date:
            todays_collection = todays_collection + int(fee.amount)

    rr = Running_batch_check(0, user)
    total_income = addmission_sales + packege_sales

    todays_enquiry = Front_enquiry_data.objects.filter(ins = ins, visited_date=format_date)
    todays_addmission = Front_student_course_batch_data.objects.filter(ins = ins, addmission_date=format_date)

    all_employe = Master_employee_data.objects.filter(ins = ins)
    all_call_logs = Front_call_logs.objects.filter(ins = ins).count()
    all_external_student = Add_New_Student.objects.count()
    assign1 = Assign_Test_Series_Institute_Student.objects.filter(date=format_date)
    assign2 = Assign_Test_Series_External_Student.objects.filter(date=format_date)
    test_income = 0
    for i in assign1:
        test_income += int(i.paid_fee)
    for i in assign2:
        test_income += int(i.paid_fee)
    total_test = len(assign1) + len(assign2)
    assign1 = Assign_Quiz_Institute_Student.objects.filter(date=format_date)
    assign2 = Assign_Quiz_External_Student.objects.filter(date=format_date)
    total_quiz = len(assign1) + len(assign2)
    quiz_income = 0
    for i in assign1:
        quiz_income += int(i.paid_fee)
    for i in assign2:
        quiz_income += int(i.paid_fee)
    aa = ExamInvoiceGenerate.objects.filter(date=format_date)
    aa1 = Front_student_pay_fee.objects.filter(ins = ins, payment_date=format_date)

    Tday_sale = 0
    Mnth_sale = 0
    for ii in aa:
        Tday_sale = Tday_sale + int(ii.paid_fee)
    for jj in aa1:
        Tday_sale = Tday_sale + int(jj.amount)
    for pp in previous_date:
        bb = ExamInvoiceGenerate.objects.filter(date=pp)
        bb1 = Front_student_pay_fee.objects.filter(ins = ins, payment_date=pp)
        for ii in bb:
            Mnth_sale = Mnth_sale + int(ii.paid_fee)
        for jj in bb1:
            Mnth_sale = Mnth_sale + int(jj.amount)
    data45 = []
    for dte in previous_date:
        coursesell = Front_student_pay_fee.objects.filter(ins = ins, payment_date=dte)
        examsell = ExamInvoiceGenerate.objects.filter(date=dte)
        amount = 0
        eamount = 0
        for i in coursesell:
            amount += int(i.amount)
        for j in examsell:
            eamount += int(j.paid_fee)

        ddtt = datetime.strptime(str(dte), '%d/%m/%Y').strftime("%Y-%m-%d")
        x = (('y', ddtt), ('a', amount), ('b', eamount))
        data45.append(dict(x))

    #########lIBRARY ############
    total_book = 0
    all_category = Master_catbook_data.objects.filter(ins = ins).count()
    all_issued_book = Library_Issue_Book.objects.filter(ins = ins, status='Issued').count()
    all_books = Master_book_data.objects.filter(ins = ins).order_by('-id')
    total_ebook = Master_E_Book.objects.filter(ins = ins).count()
    all_un_cat_book = Master_book_data.objects.filter(ins = ins, category=None, subcategory=None)
    todys_issued_book = Library_Issue_Book.objects.filter(ins = ins, issue=format_date, status='Issued').count()
    todays_return_book = Library_Issue_Book.objects.filter(ins = ins, Return=format_date, status='Returned').count()

    for book in all_books:
        total_book = total_book + int(book.copies)

    per1, per2, per4 = 0, 0, 0

    if total_book != 0:
        per1 = round((all_issued_book * 100) / total_book)
        per2 = round((todys_issued_book * 100) / total_book)
        per4 = round((todays_return_book * 100) / total_book)

    all_doc = Front_document_files.objects.filter(ins = ins)
    receipts = Front_student_pay_fee.objects.filter(ins = ins).count()
    receipts2 = ExamInvoiceGenerate.objects.count()
    all_receipts = receipts + receipts2
    cancel_add = Front_student_data.objects.filter( ins = ins, status='cancal').count()
    close_enq = Front_enquiry_data.objects.filter(ins = ins, status='close').count()
    open_enquiry = Front_enquiry_data.objects.filter(ins = ins, status='open')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    number1 = int(''.join(date_reverse))

    pv_f = 0
    up_f = 0
    for fdate in open_enquiry:
        follow_date = fdate.follow_up_date
        follow_date_split = follow_date.split('/')

        follow_date_reverse = follow_date_split[3::-1]
        number2 = int(''.join(follow_date_reverse))

        if number2 < number1:
            pv_f = pv_f + 1
        if number2 >= number1:
            up_f = up_f + 1
    import os
    ll = []

    context = {
        "all_students": all_students, "all_course": all_course, 'data45': data45,
        "all_enquiry": all_enquiry, "data": data, "addmission_sales": addmission_sales,
        "upcoming_amount": upcoming_amount, "todays_collection": todays_collection,
        "todays_enquiry": todays_enquiry.count(), "todays_addmission": todays_addmission.count(),
        "running_batch": len(rr), "todays_followup": todays_followup,
        "tcall": cor_vise_t_enq, "mcall": cor_vise_m_enq,
        "all_employe": all_employe, "ins_data": Institute_data(request.user), "admin": admin_show(),
        "all_call_logs": all_call_logs, "all_external_student": all_external_student, "packege_sales": packege_sales,
        "total_income": total_income, 'todays_test': total_test, 'todays_quiz': total_quiz,
        'quiz_income': quiz_income, 'test_income': test_income, "all_category": all_category, "total_book": total_book,
        "total_ebook": total_ebook, "all_un_cat_book": len(all_un_cat_book), "all_issued_book": all_issued_book,
        "todys_issued_book": todys_issued_book, "todays_return_book": todays_return_book,
        "per1": per1, "per2": per2, "per4": per4, "li": li, "tsale": today_amount, "msale": amount_this_month
        , "tosale": amount_overall, "all_doc": all_doc.count(), "all_receipts": all_receipts, "cancel_add": cancel_add
        , "close_enq": close_enq, "upcoming_fup": up_f, "previous_fup": pv_f, "Tday_sal": Tday_sale,
        "Mnth_sale": Mnth_sale, "YEAR_SALES": Total_Year_Sales(ins), "five": Five_upcoming_follow_ups(user),
        "lfive": len(Five_upcoming_follow_ups(user))

    }

    return render(request, 'Inst/Dashboard.html', context)


def Delete_All(request, num, type):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if type == "Fee_Type":
        data = Master_fee_type_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "User":
        data = User.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Course":
        data = Master_course_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Subject":
        data = Master_subject_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Medium":
        data = Master_medium_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "FeePackege":
        data = Master_fee_packege_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Designation":
        data = Master_designation_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "MakeInstallment":
        fee = Master_fee_packege_data.objects.get(id=num)
        data = Master_make_installment_data.objects.filter(ins = ins, packege=fee)
        if request.user.is_staff:
            data.delete()

    if type == "SenderId":
        data = Master_Sender_ID.objects.get(id=num)
        if not data.smstemplate_set.all():
            if request.user.is_staff:
                data.delete()

    if type == "SmsTemp":
        n = 0
        data = SMSTemplate.objects.get(id=num)
        t = Auto_SMS_Settings_data.objects.filter(sms_new_add=data).first()
        if t:
            n = 1
            t.new_addmission = False
            t.save()
        t = Auto_SMS_Settings_data.objects.filter(sms_student_fee=data).first()
        if t:
            n = 1
            t.student_fees = False
            t.save()

        t = Auto_SMS_Settings_data.objects.filter(sms_fee_reminder=data).first()
        if t:
            n = 1
            t.fee_reminder = False
            t.save()

        t = Auto_SMS_Settings_data.objects.filter(sms_student_bday=data).first()
        if t:
            n = 1
            t.student_bday = False
            t.save()

        t = Auto_SMS_Settings_data.objects.filter(sms_emp_bday=data).first()
        if t:
            n = 1
            t.emp_bday = False
            t.save()

        t = Auto_SMS_Settings_data.objects.filter(sms_new_ts_asign=data).first()
        if t:
            n = 1
            t.new_ts_asign = False
            t.save()

        if request.user.is_staff:
            data.delete()
        if n == 1:
            return redirect("Master:auto_sms_settings")

    if type == "Batch":
        data = Master_batch_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Student":
        data = Front_student_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Enquiry":
        data = Front_enquiry_data.objects.get(id=num)
        if request.user.is_staff:
            if request.user.is_staff:
                data.delete()

    if type == "External":
        data = Front_call_logs.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    if type == "Holiday":
        data = Master_holiday_data.objects.get(id=num)
        if request.user.is_staff:
            data.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def Add_to_data(request, type):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if type == "Fee_Type":
        all_course = Master_course_data.objects.filter(ins = ins)
        if request.method == "POST":
            fee_type = request.POST['fee_name']
            today = date.today()
            format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
            Master_fee_type_data.objects.create(name=fee_type, created_date=format_date)
            return redirect('master_fee')

        return render(request, 'Inst/master_add_fee_type.html', {"all_course": all_course, "admin": admin_show()
            , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                                 "lfive": len(Five_upcoming_follow_ups(user))})

    if type == "Subject":
        courses = Master_course_data.objects.filter(ins = ins)

        if request.method == "POST":
            name = request.POST['subject']
            cor = request.POST['course']
            today = date.today()
            format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
            sub_course = Master_course_data.objects.filter(id=cor).first()
            Master_subject_data.objects.create(ins = ins, course=sub_course, name=name
                                               , created_date=format_date)
            return redirect('master_subject')

        return render(request, 'Inst/master_add_subject.html', {"courses": courses, "admin": admin_show()
            , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                                "lfive": len(Five_upcoming_follow_ups(user))})

    if type == "Batch":
        courses = Master_course_data.objects.filter(ins = ins)

        if request.method == "POST":
            co = request.POST['course']
            name = request.POST['batch']
            start = request.POST['start']
            end = request.POST['end']
            x = start.split('/')
            if len(x[0]) < 2:
                y = x.pop(0)
                y = '0' + y
                x.insert(0, y)
            if len(x[1]) < 2:
                y = x.pop(1)
                y = '0' + y
                x.insert(1, y)
            x = '/'.join(x)
            start = x
            x = end.split('/')
            if len(x[0]) < 2:
                y = x.pop(0)
                y = '0' + y
                x.insert(0, y)
            if len(x[1]) < 2:
                y = x.pop(1)
                y = '0' + y
                x.insert(1, y)
            x = '/'.join(x)
            end = x
            today = date.today()
            format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
            course = Master_course_data.objects.filter(id=co).first()
            dd = request.POST.getlist('day')
            short_nm = '-'.join(dd)

            data = Master_batch_data.objects.create(ins = ins, course=course, name=name, start_date=start, end_date=end,
                                                    created_date=format_date, batch_shot_name=short_nm,
                                                    )

            return redirect('Master:last_date', data.id)

        return render(request, 'Inst/master_add_batch.html', {"courses": courses, "admin": admin_show()
            , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                              "lfive": len(Five_upcoming_follow_ups(user))})

    return redirect(request.META.get('HTTP_REFERER'))


def Master_Edit_for_all(request, num, type):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if request.method == "POST":
        d = request.POST
        if type == 'Course':
            data = Master_course_data.objects.filter(id=num).first()
            name = d['course']
            medium = d['medium']
            short_name = d['short_name']
            data.name = name
            data.medium = medium
            data.short_name = short_name
            data.save()
            return redirect(request.META.get('HTTP_REFERER'))
        if type == 'FeeType':
            data = Master_fee_type_data.objects.filter(id=num).first()
            name = d['fee']
            data.name = name
            data.save()
            return redirect(request.META.get('HTTP_REFERER'))

        if type == 'SenderId':
            data = Master_Sender_ID.objects.filter(id=num).first()
            name = d['sender']
            data.name = name
            data.save()
            return redirect(request.META.get('HTTP_REFERER'))

    if type == 'Batch':
        all_courses = Master_course_data.objects.filter(ins = ins)
        data = Master_batch_data.objects.filter(id=num).first()
        sn = data.batch_shot_name.split('-')
        if request.method == "POST":
            d = request.POST
            c = d['course']
            course = Master_course_data.objects.filter(id=c).first()
            name = d['batch']
            bl = d.getlist('day')
            batch_shot_name = '-'.join(bl)
            start_date = d['start']
            end_date = d['end']
            data.course = course
            data.name = name
            data.batch_shot_name = batch_shot_name
            data.start_date = start_date
            data.end_date = end_date
            data.save()
            return redirect('Master:master_batch')

        return render(request, 'Inst/master_edit_batch.html', {"data": data, "sn": sn, "all_courses": all_courses
            , "admin": admin_show(), "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                               "lfive": len(Five_upcoming_follow_ups(user))})
    if type == 'Feepackege':
        li = []
        li2 = []
        data = Master_fee_packege_data.objects.filter(id=num).first()
        all_feetype = Master_fee_type_data.objects.all()
        pac_fee_type = data.master_fee_type_packege_data_set.all()
        for p in pac_fee_type:
            li.append(p.fee_type)
        for fee in all_feetype:
            if fee.name in li:
                pass
            else:

                li2.append(fee)
        if request.method == "POST":
            li3 = []
            d = request.POST
            packege_name = d['packege_name']
            single_discount = request.POST['single_discount']
            total = d['total']
            data.name = packege_name
            data.discount_for_single = single_discount
            data.total_fee = total
            data.save()
            fees = d.getlist('fee')
            for i in fees:
                li3.append(d[i])
            if request.user.is_staff:
                pac_fee_type.delete()

            for j in range(len(fees)):
                Master_fee_type_packege_data.objects.create(ins = ins, course=data, fee_type=fees[j], fee=li3[j])

            return redirect('Master:master_packege')

        return render(request, 'Inst/edit_fee_packege.html',
                      {"data": data, "all_feetype": all_feetype, "pac_fee_type": pac_fee_type
                          , "li2": li2, "l": len(li2), "admin": admin_show()
                          , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                       "lfive": len(Five_upcoming_follow_ups(user))})

    if type == "SmsTemp":
        data = SMSTemplate.objects.filter(id=num).first()
        form = SMS_Template_Form(instance=data)
        if request.method == "POST":
            form = SMS_Template_Form(request.POST or None, instance=data)
            if form.is_valid():
                instance = form.save()
                instance.save()
                return redirect("Master:master_stemp")
        return render(request, 'Inst/master_edit_sms_temp.html',
                      {"form": form, "admin": admin_show(), "ins_data": Institute_data(request.user)
                          , "five": Five_upcoming_follow_ups(user)})

    return redirect(request.META.get('HTTP_REFERER'))


def Edit_installment_last_date(request, num):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = Master_batch_data.objects.filter(id=num).first()
    data2 = data.front_student_course_batch_data_set.all()

    if request.method == "POST":
        d = request.POST
        li = []
        for ins in data.master_installment_last_date_set.all():
            nam = "install" + str(ins.id)
            dd = d[nam]
            ins.last_date = dd
            li.append(dd)
            ins.save()
        a = 0

        for st in data2:
            for inst in st.front_student_fee_installment_data_set.all():
                inst.installment_last_date = li[a]
                inst.save()
                a = a + 1
            a = 0
        return redirect('Master:master_batch')

    return render(request, 'Inst/master_edit_last_date.html', {"data": data, "admin": admin_show(),
                                                               "ins_data": Institute_data(request.user),
                                                               "five": Five_upcoming_follow_ups(user),
                                                               "lfive": len(Five_upcoming_follow_ups(user))})


def Edit_installment(request, num):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = Master_fee_packege_data.objects.filter(id=num).first()
    total = int(data.total_fee)
    data2 = data.master_make_installment_data_set.all()
    if request.method == "POST":
        d = request.POST
        for i in data2:
            nam = 'name' + str(i.id)
            per = int(d[nam])
            amount = (total * per) / 100
            i.amount = amount
            i.percentage = per
            i.save()
        return redirect('Master:master_details_packege', data.id)

    return render(request, 'Inst/master_edit_installment.html', {"data": data2, "admin": admin_show()
        , "ins_data": Institute_data(request.user)
        , "five": Five_upcoming_follow_ups(user)})


def Master_fee_type(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_type = Master_fee_type_data.objects.all()
    if request.method == "POST":
        fee_type = request.POST['fee']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_fee_type_data.objects.create(name=fee_type, created_date=format_date)

    return render(request, 'Inst/master_fee_type.html', {"all_type": all_type, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Master_course_module(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_courses = Master_course_data.objects.filter(ins = ins)
    mediums = Master_medium_data.objects.all()
    if request.method == "POST":
        name = request.POST['course']
        med = request.POST['medium']
        short_name = request.POST['short_name']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_course_data.objects.create(ins = ins,name=name, medium=med, created_date=format_date
                                          , short_name=short_name)

    return render(request, 'Inst/master_course_module.html', {"all_courses": all_courses, "mediums": mediums,
                                                              "admin": admin_show(), "ins_data": Institute_data(request.user),
                                                              "five": Five_upcoming_follow_ups(user),
                                                              "lfive": len(Five_upcoming_follow_ups(user))})


def Master_subject(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_courses = Master_course_data.objects.filter(ins = ins)
    return render(request, 'Inst/master_subject.html', {"all_courses": all_courses, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Master_fee_packege(request):

    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_packege = Master_fee_packege_data.objects.filter(ins = ins)
    return render(request, 'Inst/master_fee_packege.html', {"all_packege": all_packege, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Master_add_fee_packege(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    pack = []
    for p in all_course:
        d = p.master_fee_packege_data_set.all()
        if d:
            continue
        pack.append(p)
    all_feetype = Master_fee_type_data.objects.all()
    fee_id = []
    for i in all_feetype:
        fee_id.append(int(i.id))
    if request.method == "POST":
        c = request.POST['course']
        packege_name = request.POST['packege_name']
        total = request.POST['total']
        single_discount = request.POST['single_discount']

        course = Master_course_data.objects.filter(id=c).first()
        data = Master_fee_packege_data.objects.create(ins = ins, course=course, name=packege_name,
                                                      discount_for_single=single_discount,
                                                      total_fee=total)
        li1 = []
        li = request.POST.getlist('fee')

        course_packege = Master_fee_packege_data.objects.filter(id=data.id).first()
        for i in li:
            li1.append(request.POST[i])
        for j in range(len(li)):
            Master_fee_type_packege_data.objects.create(ins = ins, course=course_packege, fee_type=li[j], fee=li1[j])

        return redirect('Master:master_packege')
    return render(request, 'Inst/master_add_packege.html', {"all_course": pack,
                                                            "all_feetype": all_feetype, 'fee_id': fee_id,
                                                            "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Number_of_installment(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_packege = Master_fee_packege_data.objects.filter(ins = ins)
    pack = []
    for p in all_packege:
        d = p.master_make_installment_data_set.all()
        if d:
            continue
        pack.append(p)
    if request.method == "POST":
        course_packege = request.POST['course_packege']
        number = request.POST['number']

        return redirect('Master:master_installment', course_packege, number)

    return render(request, 'Inst/master_install.html', {"pack": pack, "all_packege": all_packege, "admin": admin_show(),
                                                        "ins_data": Institute_data(request.user),
                                                        "five": Five_upcoming_follow_ups(user),
                                                        "lfive": len(Five_upcoming_follow_ups(user))})


def Master_make_installment(request, course_packege, number):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_fee_packege_data.objects.get(id=course_packege)
    data1 = Master_fee_packege_data.objects.filter(id=course_packege).first()
    total_fee = int(data.total_fee)
    n = int(number)
    li = []
    for i in range(1, n + 1):
        li.append(i)
    if request.method == "POST":

        ins1 = []
        for num in range(1, int(number) + 1):
            ins1.append(request.POST[str(num)])
        a = 1
        for j in range(len(ins1)):
            na = "installment " + str(a)
            per = int(ins1[j])
            amount = (total_fee * per) / 100
            Master_make_installment_data.objects.create(ins = ins, packege=data1, name=na,
                                                        percentage=ins1[j], amount=amount)
            a += 1
        return redirect('Master:master_packege')

    return render(request, 'Inst/master_make_installment.html', {"data": data, "li": li, "admin": admin_show(),
                                                                 "ins_data": Institute_data(request.user),
                                                                 "five": Five_upcoming_follow_ups(user),
                                                                 "lfive": len(Five_upcoming_follow_ups(user))})


def Master_fee_packege_details(request, fid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = Master_fee_packege_data.objects.get(id=fid)
    fee_id = Master_fee_packege_data.objects.filter(id=fid).first()
    ins_list = []

    for i in fee_id.master_make_installment_data_set.all():
        ins_list.append(int(i.percentage))

    return render(request, 'Inst/master_packege_details.html', {"data": data, "fee_id": fee_id, "ins_list": ins_list,
                                                                "admin": admin_show(), "ins_data": Institute_data(request.user),
                                                                "five": Five_upcoming_follow_ups(user),
                                                                "lfive": len(Five_upcoming_follow_ups(user))})


def Master_batch(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    all_batches = Master_batch_data.objects.filter(ins = ins)
    return render(request, 'Inst/master_all_batch.html', {"all_course": all_course, "all_batches"
    : all_batches, "admin": admin_show(), "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                          "lfive": len(Five_upcoming_follow_ups(user))})


def Master_last_date_ins(request, cid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    batch_data = Master_batch_data.objects.get(id=cid)
    course_id = batch_data.course.id
    course_data = Master_course_data.objects.filter(id=course_id).first()
    packege_data = Master_fee_packege_data.objects.filter(ins = ins, course=course_data).first()
    if request.method == "POST":

        batch = Master_batch_data.objects.filter(id=cid).first()

        for ins1 in packege_data.master_make_installment_data_set.all():
            ins_data = Master_make_installment_data.objects.filter(id=ins1.id).first()
            name = "install" + str(ins1.id)
            last_date = request.POST[name]
            formate_last_date = datetime.strptime(str(last_date), "%Y-%m-%d").strftime('%d/%m/%Y')
            Master_installment_last_date.objects.create(ins = ins, batch=batch, installment=ins_data, last_date=formate_last_date)

        return redirect('Master:master_batch')

    return render(request, 'Inst/master_last_ins_date.html',
                  {"packege_data": packege_data, "batch_data": batch_data, "admin": admin_show()
                      , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user))})


def Master_medium(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_medium = Master_medium_data.objects.all()
    if request.method == "POST":
        medium = request.POST['medium']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_medium_data.objects.create(name=medium, created_date=format_date)

    return render(request, 'Inst/master_medium.html', {"all_medium": all_medium, "admin": admin_show(),
                                                       "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                       "lfive": len(Five_upcoming_follow_ups(user))})


def Master_designation(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_desig = Master_designation_data.objects.all()
    if request.method == "POST":
        desig = request.POST['desig']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_designation_data.objects.create(name=desig, created_date=format_date)

    return render(request, 'Inst/master_designation.html', {"all_desig": all_desig, "admin": admin_show(),
                                                            "ins_data": Institute_data(request.user),
                                                            "five": Five_upcoming_follow_ups(user),
                                                            "lfive": len(Five_upcoming_follow_ups(user))})


def Master_inventory(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    return render(request, 'Inst/master_inventory.html')


def Master_vendor(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    return render(request, 'Inst/master_vendor.html')


def Master_terms_con(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    return render(request, 'Inst/master_terms.html')


def Master_holiday(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_holiday = Master_holiday_data.objects.filter(ins = ins)
    if request.method == "POST":
        name = request.POST['holiday']
        dstart = request.POST['start']
        dend = request.POST['end']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_holiday_data.objects.create(ins = ins, name=name, start_date=dstart, end_date=dend,
                                           created_date=format_date)
        return redirect('Master:master_holiday')

    return render(request, 'Inst/master_holiday.html', {"all_holiday": all_holiday, "admin": admin_show(),
                                                        "ins_data": Institute_data(request.user),
                                                        "five": Five_upcoming_follow_ups(user),
                                                        "lfive": len(Five_upcoming_follow_ups(user))})


def Master_sms_id(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_sender_id = Master_Sender_ID.objects.all()
    if request.method == "POST":
        sender = request.POST['sender']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_Sender_ID.objects.create(name=sender, created_date=format_date)

    return render(request, 'Inst/master_sms_id.html', {"all_sender_id": all_sender_id, "admin": admin_show(),
                                                       "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                       "lfive": len(Five_upcoming_follow_ups(user))})


def Master_email_temp(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    return render(request, 'Inst/master_email_temp.html')


from .forms import *


def Create_SMS_Template(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    form = SMS_Template_Form()
    if request.method == "POST":
        form = SMS_Template_Form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("Master:master_stemp")

    return render(request, "Inst/create_sms_template.html", {'form': form, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def SMS_Templates_List(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    sms = SMSTemplate.objects.all()
    li = []
    for s in sms:
        data = Auto_SMS_Settings_data.objects.filter(sms_new_add=s)
        if data:
            li.append(s.id)

    return render(request, "Inst/sms_templates_list.html", {'sms': sms, "admin": admin_show(), 'li': li
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Master_create_library_fine(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = LateFine.objects.filter(ins = ins).first()
    if request.method == "POST":
        late_fine = request.POST['fine']
        if data:
            data.libraryfine = late_fine
            data.save()
        else:
            LateFine.objects.create(ins = ins, libraryfine=late_fine)
        return redirect('Master:master_book_fine')

    return render(request, 'Inst/master_book_fine.html',
                  {"data": data, "admin": admin_show(), "ins_data": Institute_data(request.user),
                   "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


###################### Functions For Students############################

def Admin_all_students(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_student = Front_student_data.objects.filter(ins = ins, status='selected')
    return render(request, 'Inst/admin_all_students.html', {"all_student": all_student, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_todays_addmission(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
    todays_add = Front_student_course_batch_data.objects.filter(ins = ins, addmission_date=format_date)
    return render(request, 'Inst/admin_todays_addmission.html', {"todays_add": todays_add, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_Fee_Receipt(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_student_pay_fee.objects.filter(ins = ins).order_by('-id')
    return render(request, 'Inst/admin_all_receipts.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Student_fee_report(request, cor, bat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    course = False
    batch = False
    data = False
    if cor != '0':
        course = Master_course_data.objects.filter(id=cor).first()
    if bat != '0':
        batch = Master_batch_data.objects.filter(id=bat).first()
        data = Front_student_course_batch_data.objects.filter(ins = ins, course=course, Batch=batch)
    return render(request, 'Inst/admin_students_fee_report.html',
                  {"data": data, "all_course": all_course, "course": course,
                   "batch": batch, "admin": admin_show(),
                   "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_open_enquiry(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_enquiry_data.objects.filter(ins = ins, status='open')
    return render(request, 'Inst/admin_open_enquiry.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_close_enquiry(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_enquiry_data.objects.filter(ins = ins, status='close')
    return render(request, 'Inst/admin_close_enquiry.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_todays_enquiry(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_enquiry_data.objects.filter(ins = ins, visited_date=format_date)

    return render(request, 'Inst/admin_todays_enquiry.html', {"data": data, "admin": admin_show(),
                                                              "ins_data": Institute_data(request.user),
                                                              "five": Five_upcoming_follow_ups(user),
                                                              "lfive": len(Five_upcoming_follow_ups(user))})



def Admin_All_cancal_addmission(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_student = Front_student_data.objects.filter(ins = ins, status='cancal')
    return render(request, 'Inst/admin_all_cancal_students.html', {"all_student": all_student, "admin": admin_show(),
                                                                   "ins_data": Institute_data(request.user),
                                                                   "five": Five_upcoming_follow_ups(user),
                                                                   "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_External_follow_up(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_call_logs.objects.filter(ins = ins).order_by('-id')

    return render(request, 'Inst/admin_all_external_follow_up.html', {"data": data, "admin": admin_show(),
                                                                      "ins_data": Institute_data(request.user),
                                                                      "five": Five_upcoming_follow_ups(user),
                                                                      "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_todays_follow_ups(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_enquiry_data.objects.filter(ins = ins, status='open', todays_follow_up_date=format_date)
    return render(request, 'Inst/admin_todays_follow_up.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_upcoming_follow_ups(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    li = Five_upcoming_follow_ups(user)

    return render(request, 'Inst/admin_upcoming_follow_up.html', {"data": li, "admin": admin_show(),
                                                                  "ins_data": Institute_data(request.user),
                                                                  "five": Five_upcoming_follow_ups(user),
                                                                  "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_fee_reminders(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
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
                                b = b + 1
                                li.append(ins)
                                if b == 1:
                                    li5.append(stu)

    return render(request, 'Inst/admin_fee_reminders.html', {"li3": li3, "li4": li4, "li": li,
                                                             "li5": li5, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


######################## Library Functions ##################3

def Admin_All_category(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_catbook_data.objects.filter(ins = ins)
    return render(request, 'Inst/admin_all_category.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_Books(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_book_data.objects.filter(ins = ins)
    li = []
    for bk in data:
        book = Master_book_data.objects.filter(id=bk.id).first()
        da = Library_Issue_Book.objects.filter(ins = ins, book=book, status='Issued')
        if da:
            li.append(bk)
    return render(request, 'Inst/admin_all_books.html',
                  {"data": data, "li": li, "admin": admin_show(), "ins_data": Institute_data(request.user)
                      , "five": Five_upcoming_follow_ups(user)})


def Admin_All_E_books(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_E_Book.objects.filter(ins = ins)
    return render(request, 'Inst/admin_all_ebooks.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_Issued_Books(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Library_Issue_Book.objects.filter(ins = ins, status='Issued')
    return render(request, 'Inst/admin_all_issued_books.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_Issued_return_book(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Library_Issue_Book.objects.filter(ins = ins, status='Returned')
    return render(request, 'Inst/admin_all_issued_return_book.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_subcategory(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_catbook_data.objects.filter(ins = ins)
    return render(request, 'Inst/admin_all_subcategory.html', {"data": data, "admin": admin_show(),
                                                               "ins_data": Institute_data(request.user),
                                                               "five": Five_upcoming_follow_ups(user),
                                                               "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_uncat_book(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Master_book_data.objects.filter(ins = ins, category=None, subcategory=None)
    li = []
    for bk in data:
        book = Master_book_data.objects.filter(id=bk.id).first()
        da = Library_Issue_Book.objects.filter(ins = ins, book=book, status='Issued')
        if da:
            li.append(bk)
    return render(request, 'Inst/admin_all_uncat_book.html', {"data": data, "li": li, "admin": admin_show(),
                                                              "ins_data": Institute_data(request.user),
                                                              "five": Five_upcoming_follow_ups(user),
                                                              "lfive": len(Five_upcoming_follow_ups(user))})


################# Frontdesk Functions #################

def Admin_previous_follow_ups(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
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

    return render(request, 'Inst/admin_previous_follow_up.html', {"data": li, "admin": admin_show(),
                                                                  "ins_data": Institute_data(request.user),
                                                                  "five": Five_upcoming_follow_ups(user),
                                                                  "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_All_Batch_uploaded_documents(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Front_document_files.objects.filter(ins = ins).order_by('-id')
    li = []
    li2 = []
    for i in data:
        if not i.doc_file_name in li:
            li.append(i.doc_file_name)
            li2.append(i)
    return render(request, 'Inst/admin_uploaded_files.html', {"data": li2, "admin": admin_show(),
                                                              "ins_data": Institute_data(request.user),
                                                              "five": Five_upcoming_follow_ups(user),
                                                              "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_upload_new_files(request, cor):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    course = False
    rr = False
    if cor != '0':
        course = Master_course_data.objects.filter(id=cor).first()
        rr = Running_batch_check(course.id, user)

    if request.method == "POST":
        option = request.POST['option']
        document_file = request.FILES['document']
        name = request.POST['name']
        today_date = date.today()
        upload_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

        if option == 'batches':

            batch_list = request.POST.getlist('batch')
            for i in batch_list:
                batch_data = Master_batch_data.objects.filter(id=i).first()

                student_data1 = Front_student_course_batch_data.objects.filter(ins = ins, Batch=batch_data)
                for ss in student_data1:
                    ss2 = Front_student_data.objects.filter(id=ss.student.id).first()
                    Front_document_files.objects.create(ins = ins, student=ss2, document_file=document_file,
                                                        doc_name=name, upload_date=upload_date)

                Front_All_Uploaded_document.objects.create(ins = ins, batch=batch_data, doc_name=name, doc_file=document_file,
                                                           upload_date=upload_date)

        if option == 'allstudent':
            student_data = Front_student_data.objects.filter(ins = ins)
            for ss in student_data:
                ss2 = Front_student_data.objects.filter(id=ss.id).first()
                Front_document_files.objects.create(ins = ins, student=ss2, document_file=document_file, doc_name=name,
                                                    upload_date=upload_date)
        return redirect('Master:admin_all_upload_files')

    return render(request, 'Inst/admin_upload_new_file.html', {"course": course, "all_course": all_course, 'cor': cor,
                                                               "rr": rr, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_notification_for_batch(request, cour, batch):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    Sms_Templates = False
    course = False
    Batch = False
    show = False
    if cour != '0':
        course = Master_course_data.objects.filter(id=cour).first()
    if cour != '0' and batch != '0':
        Sms_Templates = SMSTemplate.objects.all()
        if not Sms_Templates:
            show = True

        Batch = Master_batch_data.objects.filter(id=batch).first()
        data = Front_student_course_batch_data.objects.filter(ins = ins, course=course, Batch=Batch)

        if request.method == "POST":
            d = request.POST
            temp = d['sms_select']
            by = d['by']
            dat = Send_Notification_student(temp, by, data,request.user)
            print(dat)
            if not dat:
                return redirect("Master:sms_fail")

            return redirect("Master:master_deshboard")

    return render(request, 'Inst/admin_notification_for_batch.html', {"all_course": all_course,
                                                                      "course": course, "batch": Batch,
                                                                      'Sms_Templates': Sms_Templates, "ForBatch": True
        , "admin": admin_show(),"student":True, "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                                                                      "lfive": len(Five_upcoming_follow_ups(user)),"show":show})


def Admin_Select_student_for_notifi(request, cour, batch):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    course = False
    Batch = False
    total = False
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    if cour != '0':
        course = Master_course_data.objects.filter(id=cour).first()
    if batch != '0':
        Batch = Master_batch_data.objects.filter(id=batch).first()
        total = Front_student_course_batch_data.objects.filter(ins = ins, Batch=Batch).count()
        if request.method == "POST":
            d = request.POST
            stuid = d.getlist('stuid')
            collection = '-'.join(stuid)
            return redirect("Master:admin_notification_for_single", collection)

    return render(request, 'Inst/admin_select_student.html', {"course": course, "all_course": all_course,
                                                              "Batch": Batch, "total": total, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_notification_for_individual(request, ndata):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    show = False
    Sms_Templates = SMSTemplate.objects.all()
    if not Sms_Templates:
        show = True
    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']
        li = ndata.split('-')
        Dat = []
        for i in li:
            data = Front_student_course_batch_data.objects.filter(id=i).first()
            Dat.append(data)
        dta = Send_Notification_student(temp, by, Dat,request.user)
        if not dta:
            return redirect("Master:sms_fail")
        return redirect('Master:admin_select_student', '0', '0')
    return render(request, 'Inst/admin_notification_for_batch.html',
                  {"Sms_Templates": Sms_Templates, "admin": admin_show(),"student":True
                      , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user)),"show":show})


def Admin_notification_for_all_staff(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    show = False
    Sms_Templates = SMSTemplate.objects.all()
    if not Sms_Templates:
        show = True
    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']

        staff_data = Master_employee_data.objects.filter(ins = ins)
        dta = Send_Notification_staff(temp, by, staff_data,request.user)
        if not dta:
            return redirect("Master:sms_fail")

    return render(request, 'Inst/admin_notification_for_batch.html', {"Sms_Templates": Sms_Templates,
                                                                       "admin": admin_show(),
                                                                      "ins_data": Institute_data(request.user),
                                                                      "five": Five_upcoming_follow_ups(user),
                                                                      "lfive": len(Five_upcoming_follow_ups(user)),"show":show})


def Admin_notification_for_single_staff(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    Sms_Templates = SMSTemplate.objects.all()
    all_staff = Master_employee_data.objects.filter(ins = ins)
    if request.method == "POST":
        d = request.POST
        temp = d['sms_select']
        by = d['by']
        staff_id = d['staff_id']
        staff_data = Master_employee_data.objects.filter(id=staff_id)
        dta = Send_Notification_staff(temp, by, staff_data,request.user)
        if not dta:
            return redirect("Master:sms_fail")

    return render(request, 'Inst/admin_notification_for_single_staff.html', {"Sms_Templates": Sms_Templates,
                                                                             "all_staff": all_staff,
                                                                             "admin": admin_show(),
                                                                             "ins_data": Institute_data(request.user),
                                                                             "five": Five_upcoming_follow_ups(user),
                                                                             "lfive": len(Five_upcoming_follow_ups(user))})


############# Employee Functions #################

def Admin_add_employe(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    IdError = False
    all_designation = Master_designation_data.objects.all()
    form = AddEmployeForm()
    if request.method == "POST":

        desig = request.POST['desig']
        print("hello", desig)
        form = AddEmployeForm(request.POST, request.FILES)
        if form.is_valid():
            print("hello")
            data = form.save(commit=False)
            Eid = data.employee_id
            Pre = Master_employee_data.objects.filter(employee_id=Eid).first()
            if not Pre:
                data.designation = desig
                data.ins = ins
                data.save()
                return redirect('Master:master_employee')
            IdError = True
    return render(request, 'Inst/admin_add_employe.html',
                  {"form": form, "all_designation": all_designation, "admin": admin_show(), "IdError": IdError
                      , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user))})


def Master_employee(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_employee = Master_employee_data.objects.filter(ins = ins)

    return render(request, 'Inst/master_employee.html', {"all_employee": all_employee, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_VED_employee(request, num, type):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    IdError = False
    data = Master_employee_data.objects.filter(id=num).first()
    data1 = Master_employee_data.objects.filter(id=num).first()
    dd = data.designation
    if type == 'Delete':
        if request.user.is_staff:
            data.delete()
        return redirect('Master:master_employee')
    if type == 'Edit':
        all_designation = Master_designation_data.objects.all()
        form = AddEmployeForm(instance=data)
        if request.method == "POST":
            desig = request.POST['desig']
            form = AddEmployeForm(request.POST or None, request.FILES or None, instance=data)
            if form.is_valid():
                data = form.save(commit=False)
                Eid = data.employee_id
                Pre = Master_employee_data.objects.filter(employee_id=Eid).first()
                print(Pre, data1.employee_id, data.employee_id)
                if (Pre and Eid == data1.employee_id) or (Eid != data1.employee_id and Pre == None):
                    print("Today")
                    data.designation = desig
                    data.save()
                    return redirect('Master:admin_VED_employee', data.id, 'View')
                IdError = True

        return render(request, 'Inst/admin_add_employe.html',
                      {"data": data, "form": form, "all_designation": all_designation, 'IdError': IdError,
                       "Edit": True, "dd": dd, "admin": admin_show()
                          , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                       "lfive": len(Five_upcoming_follow_ups(user))})
    if type == "View":
        return render(request, 'Inst/admin_view_employee.html',
                      {"data": data, "admin": admin_show(), "ins_data": Institute_data(request.user)
                          , "five": Five_upcoming_follow_ups(user)})


#####################Sales Function ##################


def Admin_Course_wise_sales(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    today_date = date.today()
    previous_date = []
    amount_this_month = []
    amount_overall = []
    today_amount = []
    am = 0
    am1 = 0
    am2 = 0
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    td = int(format_date[:2])
    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    for course in all_course:
        for st in course.front_student_course_batch_data_set.all():
            all_payments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st)
            for allpay in all_payments:
                am2 = am2 + int(allpay.amount)

            tpayments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st, payment_date=format_date)
            for tpa in tpayments:
                am1 = am1 + int(tpa.amount)
            for pdate in previous_date:
                payments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st, payment_date=pdate)
                for pa in payments:
                    am = am + int(pa.amount)
        amount_this_month.append(am)
        today_amount.append(am1)
        amount_overall.append(am2)
        am1 = 0
        am = 0
        am2 = 0

    return render(request, 'Inst/admin_course_wise_sales.html', {"This_month": amount_this_month,
                                                                 "today": today_amount, "overall": amount_overall,
                                                                 "all_course": all_course, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Total_packeges_sales(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_packeges = ExamPackage.objects.all()
    total = []
    today = []
    month = []
    total_asign = []
    today_asign = []
    month_asign = []
    a = 0
    b = 0
    c = 0

    imm = 0
    emm = 0
    previous_date = []
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    tdd = int(format_date[:2])
    for i in range(tdd - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    for pak in all_packeges:
        ins_students = Assign_Test_Series_Institute_Student.objects.filter(real=pak)
        itt = Assign_Test_Series_Institute_Student.objects.filter(real=pak).count()
        ett = Assign_Test_Series_External_Student.objects.filter(real=pak).count()
        total_asign.append(itt + ett)
        itd = Assign_Test_Series_Institute_Student.objects.filter(real=pak, date=format_date).count()
        etd = Assign_Test_Series_External_Student.objects.filter(real=pak, date=format_date).count()
        today_asign.append(itd + etd)
        for pdate in previous_date:
            imm = imm + Assign_Test_Series_Institute_Student.objects.filter(real=pak, date=pdate).count()
            emm = emm + Assign_Test_Series_External_Student.objects.filter(real=pak, date=pdate).count()
            monthly_sales = imm + emm

        for st in ins_students:

            payments = ExamInvoiceGenerate.objects.filter(exam=st)

            for pay in payments:
                b = b + int(pay.paid_fee)

            tpayments = ExamInvoiceGenerate.objects.filter(exam=st, date=format_date)
            for tpay in tpayments:
                a = a + int(tpay.paid_fee)

            for pdate in previous_date:
                mpayments = ExamInvoiceGenerate.objects.filter(exam=st, date=pdate)
                for mpay in mpayments:
                    c = c + int(mpay.paid_fee)

        ex_students = Assign_Test_Series_External_Student.objects.filter(real=pak)

        for est in ex_students:
            epayments = ExamInvoiceGenerate.objects.filter(o_exam=est)
            for epay in epayments:
                b = b + int(epay.paid_fee)

            etpayments = ExamInvoiceGenerate.objects.filter(o_exam=est, date=format_date)
            for etpay in etpayments:
                a = a + int(etpay.paid_fee)

            for pdate in previous_date:
                empayments = ExamInvoiceGenerate.objects.filter(o_exam=est, date=pdate)
                for empay in empayments:
                    c = c + int(empay.paid_fee)
        today.append(a)
        a = 0
        total.append(b)
        b = 0
        month.append(c)
        c = 0
        month_asign.append(monthly_sales)
        imm = 0
        emm = 0

    context = {"today": today, "total": total, "month": month, "today_asign": today_asign, "total_asign": total_asign,
               "month_asign": month_asign, "admin": admin_show(), "ins_data": Institute_data(request.user),
               "all_packege": all_packeges, "five": Five_upcoming_follow_ups(user),
               "lfive": len(Five_upcoming_follow_ups(user))}

    return render(request, 'Inst/admin_total_packege_sales.html', context)


def Admin_Quiz_sales_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    all_packeges = QuizPackage.objects.all()
    total = []
    today = []
    month = []
    total_asign = []
    today_asign = []
    month_asign = []
    a = 0
    b = 0
    c = 0

    imm = 0
    emm = 0
    previous_date = []
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    tdd = int(format_date[:2])
    for i in range(tdd - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    for pak in all_packeges:
        ins_students = Assign_Quiz_Institute_Student.objects.filter(real=pak)
        itt = Assign_Quiz_Institute_Student.objects.filter(real=pak).count()
        ett = Assign_Quiz_External_Student.objects.filter(real=pak).count()
        total_asign.append(itt + ett)
        itd = Assign_Quiz_Institute_Student.objects.filter(real=pak, date=format_date).count()
        etd = Assign_Quiz_External_Student.objects.filter(real=pak, date=format_date).count()
        today_asign.append(itd + etd)
        for pdate in previous_date:
            imm = imm + Assign_Quiz_Institute_Student.objects.filter(real=pak, date=pdate).count()
            emm = emm + Assign_Quiz_External_Student.objects.filter(real=pak, date=pdate).count()
            monthly_sales = imm + emm

        for st in ins_students:

            payments = ExamInvoiceGenerate.objects.filter(quiz=st)

            for pay in payments:
                b = b + int(pay.paid_fee)

            tpayments = ExamInvoiceGenerate.objects.filter(quiz=st, date=format_date)
            for tpay in tpayments:
                a = a + int(tpay.paid_fee)

            for pdate in previous_date:
                mpayments = ExamInvoiceGenerate.objects.filter(quiz=st, date=pdate)
                for mpay in mpayments:
                    c = c + int(mpay.paid_fee)

        ex_students = Assign_Quiz_External_Student.objects.filter(real=pak)

        for est in ex_students:
            epayments = ExamInvoiceGenerate.objects.filter(o_quiz=est)
            for epay in epayments:
                b = b + int(epay.paid_fee)

            etpayments = ExamInvoiceGenerate.objects.filter(o_quiz=est, date=format_date)
            for etpay in etpayments:
                a = a + int(etpay.paid_fee)

            for pdate in previous_date:
                empayments = ExamInvoiceGenerate.objects.filter(o_quiz=est, date=pdate)
                for empay in empayments:
                    c = c + int(empay.paid_fee)
        today.append(a)
        a = 0
        total.append(b)
        b = 0
        month.append(c)
        c = 0
        month_asign.append(monthly_sales)
        imm = 0
        emm = 0

    context = {"today": today, "total": total, "month": month, "today_asign": today_asign, "total_asign": total_asign,
               "month_asign": month_asign, "admin": admin_show(), "ins_data": Institute_data(request.user),
               "all_packege": all_packeges, "five": Five_upcoming_follow_ups(user),
               "lfive": len(Five_upcoming_follow_ups(user))}

    return render(request, 'Inst/admin_quiz_packege_sales.html', context)


################## Reports Functions###############
def Admin_Due_fee_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_batch = Master_batch_data.objects.filter(ins = ins)
    today_date = date.today()
    li2 = []
    li3 = []
    li4 = []

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
    return render(request, 'Inst/admin_due_fee_installment_report.html', {"li3": li3, "li4": li4, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_upcoming_fee_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_batch = Master_batch_data.objects.filter(ins = ins)
    today_date = date.today()
    li2 = []
    li3 = []
    li4 = []

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
            if stu.fee_after_pay != '0':
                for ins in stu.front_student_fee_installment_data_set.all():
                    if ins.remaining_fee != '0':
                        ins_date_split = ins.installment_last_date.split('/')
                        ins_date_reverse = ins_date_split[3::-1]
                        number2 = int(''.join(ins_date_reverse))
                        if number2 >= number1:
                            a = a + 1
                            li3.append(ins)
                            if a == 1:
                                li4.append(stu)
    return render(request, 'Inst/admin_upcoming_fee_report.html', {"li3": li3, "li4": li4, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_receivable_amount(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    over_all_amount = []
    am = 0
    for course in all_course:
        for st in course.front_student_course_batch_data_set.all():
            am = am + int(st.fee_after_pay)
        over_all_amount.append(am)
        am = 0
    return render(request, 'Inst/admin_receivable_amount.html',
                  {"li": over_all_amount, "all_course": all_course, "admin": admin_show(),
                   "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_addmission_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    today_date = date.today()
    previous_date = []
    today_add = []
    month_add = []
    overall_add = []
    sbc = 0

    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    td = int(format_date[:2])
    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    for course in all_course:
        ov = course.front_student_course_batch_data_set.count()
        overall_add.append(ov)
        sbc2 = Front_student_course_batch_data.objects.filter(ins = ins, course=course, addmission_date=format_date).count()
        today_add.append(sbc2)
        for prev in previous_date:
            sbc = sbc + Front_student_course_batch_data.objects.filter(ins = ins, course=course,
                                                                       addmission_date=prev).count()
        month_add.append(sbc)
        sbc = 0

    return render(request, 'Inst/admin_addmission_report.html', {"today": today_add, "This_month": month_add,
                                                                 "overall": overall_add, "all_course": all_course,
                                                                 "admin": admin_show(),
                                                                 "ins_data": Institute_data(request.user),
                                                                 "five": Five_upcoming_follow_ups(user),
                                                                 "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Enquiry_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    today_date = date.today()
    previous_date = []
    today_enq = []
    month_enq = []
    overall_enq = []
    sbc = 0

    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    td = int(format_date[:2])
    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    for course in all_course:
        ov = Front_enquiry_data.objects.filter(ins = ins, course = course).count()
        overall_enq.append(ov)
        sbc2 = Front_enquiry_data.objects.filter(ins = ins, course=course, visited_date=format_date).count()
        today_enq.append(sbc2)
        for prev in previous_date:
            sbc = sbc + Front_enquiry_data.objects.filter(ins = ins, course=course,
                                                          visited_date=prev).count()
        month_enq.append(sbc)
        sbc = 0

    return render(request, 'Inst/admin_enquiry_report.html', {"today": today_enq, "This_month": month_enq,
                                                              "overall": overall_enq, "all_course": all_course,
                                                              "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_followup_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    today_date = date.today()
    previous_date = []
    today_fup = []
    month_fup = []
    sbc = 0

    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    td = int(format_date[:2])
    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)

    for course in all_course:
        sbc2 = Front_enquiry_data.objects.filter(ins = ins, course=course, todays_follow_up_date=format_date).count()
        today_fup.append(sbc2)
        for prev in previous_date:
            sbc = sbc + Front_enquiry_data.objects.filter(ins = ins, course=course,
                                                          todays_follow_up_date=prev).count()
        month_fup.append(sbc)
        sbc = 0

    return render(request, 'Inst/admin_followup_report.html', {"today": today_fup, "This_month": month_fup,
                                                               "all_course": all_course, "admin": admin_show(),
                                                               "ins_data": Institute_data(request.user),
                                                               "five": Five_upcoming_follow_ups(user),
                                                               "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_call_log_report(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)

    previous_date = []
    today_call = []
    month_call = []
    total_call = []
    sbc = 0
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    td = int(format_date[:2])
    for i in range(td - 1, -1, -1):
        prvate = today_date + timedelta(-i)
        pv = datetime.strptime(str(prvate), "%Y-%m-%d").strftime('%d/%m/%Y')
        previous_date.append(pv)

    for course in all_course:
        call = course.front_call_logs_set.count()
        total_call.append(call)
        sbc2 = Front_call_logs.objects.filter(ins = ins, course=course, call_date=format_date).count()
        today_call.append(sbc2)
        for prev in previous_date:
            sbc = sbc + Front_call_logs.objects.filter(ins = ins, course=course,
                                                       call_date=prev).count()
        month_call.append(sbc)
        sbc = 0

    return render(request, 'Inst/admin_call_log_report.html', {"today": today_call, "This_month": month_call,
                                                               "all_course": all_course, "overall": total_call,
                                                               "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Select_Month_year(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    if request.method == 'POST':
        d = request.POST
        month = int(d['month'])
        year = int(d['year'])
        return redirect('Master:admin_monthly_collection', month, year)
    return render(request, 'Inst/select_month_and_year.html', {"admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Monthly_Fee_collection_Report(request, mo, ye):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    li2 = ['0', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
           'October', 'November', 'December']
    am = 0
    li = []
    mo = int(mo)
    ye = int(ye)
    monthly_collection = []
    a = calendar.monthrange(ye, mo)[1]
    days = [date(ye, mo, day) for day in range(1, a + 1)]
    for d in days:
        dd = datetime.strptime(str(d), "%Y-%m-%d").strftime('%d/%m/%Y')
        li.append(dd)
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    for course in all_course:
        for st in course.front_student_course_batch_data_set.all():
            for pdate in li:
                payments = Front_student_pay_fee.objects.filter(ins = ins, student_course=st, payment_date=pdate)
                for pp in payments:
                    am = am + int(pp.amount)
        monthly_collection.append(am)
        am = 0
    month_name = li2[mo]
    return render(request, 'Inst/admin_month_wise_collection.html', {"month_name": month_name, "year": ye,
                                                                     "total": monthly_collection,
                                                                     "all_course": all_course, "admin": admin_show(),
                                                                     "ins_data": Institute_data(request.user),
                                                                     "five": Five_upcoming_follow_ups(user),
                                                                     "lfive": len(Five_upcoming_follow_ups(user))})


################################## Settings Functions ##########################

def Admin_Institute_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Institite_profile.objects.filter(id = ins.id).first()
    form = InstituteProfileForm()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    if request.method == "POST":
        form = InstituteProfileForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.save(commit=False)
            d.created_date = format_date
            d.usr = user
            d.save()
            return redirect("login")

    return render(request, 'Inst/institute_profile.html', {"form": form, "data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_New_Institute_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = None
    form = InstituteProfileForm()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    if request.method == "POST":
        form = InstituteProfileForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.save(commit=False)
            d.created_date = format_date
            d.usr = user

            d.save()
            ins = Institite_profile.objects.filter(id = d.id).first()
            Invoice_number_generate.objects.create(ins=ins,start_char='INV',number=1)
            return redirect("Master:choose_institute")

    return render(request, 'Inst/institute_profile.html', {"form": form, "data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})





def Edit_institute_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Institite_profile.objects.filter(id = ins.id).first()
    form = InstituteProfileForm(instance=data)
    if request.method == "POST":
        form = InstituteProfileForm(request.POST or None, request.FILES or None, instance=data)
        if form.is_valid():
            d = form.save()
            d.save()
            return redirect('Master:admin_institute_profile')

    return render(request, 'Inst/edit_institute_profile.html', {"form": form, "data": data, "admin": admin_show(),
                                                                "ins_data": Institute_data(request.user),
                                                                "five": Five_upcoming_follow_ups(user),
                                                                "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Auto_SMS_Setting(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    templates = SMSTemplate.objects.all()
    data = Auto_SMS_Settings_data.objects.filter().first()
    if request.method == "POST":
        d = request.POST
        li = d.getlist('check')
        if '1' in li:
            s = d['temp1']
            st = SMSTemplate.objects.filter(id=s).first()
            if data:
                data.new_addmission = True
                data.sms_new_add = st
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(new_addmission=True, sms_new_add=st)
        else:
            if data:
                data.new_addmission = False
                data.save()
        if '2' in li:
            s1 = d['temp2']
            st1 = SMSTemplate.objects.filter(id=s1).first()
            if data:
                data.student_fees = True
                data.sms_student_fee = st1
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(student_fees=True, sms_student_fee=st1)
        else:
            if data:
                data.student_fees = False
                data.save()

        if '3' in li:
            s2 = d['temp3']
            st2 = SMSTemplate.objects.filter(id=s2).first()
            if data:
                data.fee_reminder = True
                data.sms_fee_reminder = st2
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(fee_reminder=True, sms_fee_reminder=st2)
        else:
            if data:
                data.fee_reminder = False
                data.save()

        if '4' in li:
            s3 = d['temp4']
            st3 = SMSTemplate.objects.filter(id=s3).first()
            if data:
                data.student_bday = True
                data.sms_student_bday = st3
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(student_bday=True, sms_student_bday=st3)
        else:
            if data:
                data.student_bday = False
                data.save()

        if '5' in li:
            s4 = d['temp5']
            st4 = SMSTemplate.objects.filter(id=s4).first()
            if data:
                data.emp_bday = True
                data.sms_emp_bday = st4
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(emp_bday=True, sms_emp_bday=st4)
        else:
            if data:
                data.emp_bday = False
                data.save()
        if '6' in li:
            s5 = d['temp6']
            st5 = SMSTemplate.objects.filter(id=s5).first()
            if data:
                data.new_ts_asign = True
                data.sms_new_ts_asign = st5
                data.save()
            else:
                Auto_SMS_Settings_data.objects.create(new_ts_asign=True, sms_new_ts_asign=st5)
        else:
            if data:
                data.new_ts_asign = False
                data.save()

    return render(request, 'Inst/admin_auto_sms_setting.html', {"admin": admin_show(),
                                                                "ins_data": Institute_data(request.user)
        , "templates": templates, "data": data, "five": Five_upcoming_follow_ups(user),
                                                                "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Select_enquiry_students(request, cor):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_course = Master_course_data.objects.filter(ins = ins)
    students = False
    Course = False
    if cor != '0':
        Course = Master_course_data.objects.filter(id=cor).first()
        students = Front_enquiry_data.objects.filter(ins = ins, course=Course, status='open')

        if request.method == "POST":
            d = request.POST
            stuid = d.getlist('stuid')
            collection = '-'.join(stuid)

            return redirect("Master:admin_notification_enq", collection)

    return render(request, 'Inst/admin_select_enquiry_student.html',
                  {"admin": admin_show(), "all_course": all_course, "Course": Course, "students": students
                      , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user))})


def Admin_Notification_Enquiry_students(request, enq_data):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
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
            n = n + 1
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
                smsnum = ceil(len(final) / 160)
                want_sms = smsnum * len(li)
                Now = NowSMS.objects.filter().first()
                ava = int(Now.num)
                if ava < want_sms:
                    return redirect("Master:sms_fail")
                else:
                    Now.num = ava - want_sms
                    Now.save()

            SendSMS(data.mobile, final, data1.sender_id)

        return redirect('Master:admin_select_enquiry_student', '0')

    return render(request, 'Inst/admin_notification_enquiry_student.html',
                  {"admin": admin_show(), "Sms_Templates": Sms_Templates, "ins_data": Institute_data(request.user)
                      , "five": Five_upcoming_follow_ups(user)})


def Admin_Start_Invoice_number(request, option):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data2 = Invoice_number_generate.objects.filter(ins = ins).first()
    data = Invoice_number_generate.objects.filter(ins = ins).first()
    error = False
    if request.method == "POST":
        d = request.POST
        name = d['name']
        num = d['number']
        if option == "Exam":
            if not data2:
                Invoice_number_generate.objects.create(ins = ins, start_char = name, number = num)
                return redirect('Master:invoice_number', 'Exam')
            else:
                data2.start_char = d['name']
                data2.number = d['number']
                data2.save()
                return redirect('Master:invoice_number', 'Exam')
    return render(request, 'Inst/admin_start_invoice_number.html', {"admin": admin_show(), "ins_data": Institute_data(request.user)
        , "data": data, "data2": data2, "option": option
        , "five": Five_upcoming_follow_ups(user), "error":error})


def Admin_User_Management(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    employee = Master_employee_data.objects.filter(ins = ins)
    error = False
    error1 = False
    n = ''
    Employee = ''
    data = User_Management.objects.filter(ins = ins)
    today_date = date.today()
    Date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    if request.method == "POST":
        panel = request.POST['panel']
        emp = request.POST['employee']
        un = request.POST['un']
        Pass = request.POST['pass']

        Employee = Master_employee_data.objects.filter(id=emp).first()
        n = panel.capitalize()+' Panel'
        user_management_data = User_Management.objects.filter(name = n,emp =Employee).first()
        uu = User.objects.filter(username = un)

        if user_management_data:
            error = True
        elif uu:
            error1 = True
        else:

            user = User.objects.create_user(un, Employee.email, Pass)
            user.first_name = ins.id
            user.save()
            if panel == "FrontDesk":
                user.last_name = panel
                user.save()
                panel = "Frontdesk Panel"
            if panel == "Exam":
                user.last_name = panel
                user.save()
                panel = "Exam Panel"
            if panel == "Library":
                user.last_name = panel
                user.save()
                panel = "Library Panel"
            User_Management.objects.create(ins = ins, user=user, emp=Employee, name=panel,
                                           username=un, date=Date)
            return redirect("Master:user_management_settings")
    return render(request, "Inst/admin_user_management_setting.html",
                  {"admin": admin_show(), 'employee': employee, 'users': data,
                   "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user),
                   "lfive": len(Five_upcoming_follow_ups(user)),"error":error,"error1":error1,'n':n,"emp":Employee})


def Adminprofile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = Admin_profile.objects.filter(usr=request.user).first()
    return render(request, 'Inst/admin_profile.html', {"data": data, "admin": admin_show()
        , "ins_data": Institute_data(request.user), "five": Five_upcoming_follow_ups(user), "lfive": len(Five_upcoming_follow_ups(user))})


def Edit_Admin_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_admin(user):
        return redirect("login")

    data = Admin_profile.objects.filter(usr=request.user).first()
    form = Admin_profile_form(instance=data)
    if request.method == "POST":
        form = Admin_profile_form(request.POST or None, request.FILES or None, instance=data)
        if form.is_valid():
            d = form.save()
            d.save()
            return redirect('Master:admin_profile')

    return render(request, 'Inst/edit_admin_profile.html', {"form": form, "data": data, "admin": admin_show(),
                                                            "ins_data": Institute_data(request.user),
                                                            "five": Five_upcoming_follow_ups(user),
                                                            "lfive": len(Five_upcoming_follow_ups(user))})


def SmsPackReport(request):
    Sms_slip = SMS_Pack.objects.filter(usr=request.user).order_by("-id")
    now_sms = NowSMS.objects.filter().first()
    today_date = date.today()
    Date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    if request.method == "POST":
        num = request.POST['name']
        paid = int(num) * 0.17
        SMS_Pack.objects.create(usr=request.user, Number=num, paid=paid, Date=Date)
        return redirect("Master:sms_report")

    context = {
        "admin": admin_show(), "ins_data": Institute_data(request.user), "option": "Exam",
        'slips': Sms_slip, 'now': now_sms
    }
    return render(request, "Inst/sms_pack_report.html", context)



def Students_Pack_Report(request):
    all_students = Student_Pack.objects.all().order_by("-id")
    now_student = NowStudents.objects.filter().first()
    today_date = date.today()
    Date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    if request.method == "POST":
        num = request.POST['name']
        print(num)
        n = 0
        p = 0
        for i in all_students:
            n = n + int(i.Number)
        if n > 100 and n < 200:
            p = 0.50
        elif n > 200:
            p = 0.40
        else:
            p = 0.60
        paid = int(num) * p
        paid = paid * 365
        Student_Pack.objects.create(Number = num, paid = paid, Date = Date)
        return redirect("Master:student_report")

    d = {
        "option": "Exam", "students":all_students, "now":now_student, "ins_data": Institute_data(request.user),
        "admin": admin_show(),
    }
    return render(request, "Inst/student_pack_report.html", d)



def SMS_Fail(request):
    d = {
        "admin": admin_show(), "ins_data": Institute_data(request.user),
    }
    return render(request, "Inst/sms_fail.html", d)


def Student_Fail(request):
    d = {
        "admin": admin_show(), "ins_data": Institute_data(request.user),
    }
    return render(request, "Inst/student_fail.html", d)


def Start(request):
    key = KeyFeatures.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        institute = request.POST['institute']
        user = User.objects.create_user(email, "techsimplus@gmail.com", mobile)
        user.last_name = "Admin"
        user.save()
        VisitedUser.objects.create(usr=user, name=name, email=email, mobile=mobile,
                                   institute=institute)

        return redirect("login")
    return render(request, "Inst/demo.html", {'Keys': key})


