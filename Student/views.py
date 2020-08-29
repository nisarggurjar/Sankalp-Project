from django.shortcuts import render,redirect
from Frontdesk.models import *
from LibraryPanel.models import *
from ExamPanel.models import *
from .models import *
from Frontdesk.views import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate

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

def Institute_data(user):
    ins_data = Front_student_data.objects.filter(usr = user).first()
    
    return ins_data

def Show(user):
    if user.last_name == "I_Student":
        student = Front_student_data.objects.filter(usr = user).first()
    if user.last_name == "E_Student":
        print("Hello")
        student = Add_New_Student.objects.filter(usr = user).first()
    return student

def Today():
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    return format_date


def TotalTest_Question(student_data, option):
    tests = []
    if option == "Institute":
        tests = Assign_Test_Series_Institute_Student.objects.filter(student=student_data)
    if option == "External":
        tests = Assign_Test_Series_External_Student.objects.filter(student=student_data)
    exams = []
    questions = []
    marks = []
    for i in tests:
        ex = 0
        qu = 0

        sub = i.package.studentpackage_subpackage_set.all()
        for j in sub:
            exms = j.sub.studentsubpackage_mainexam_set.all()
            ex += len(exms)
            for k in exms:
                m = 0
                sec = k.main.studentmainexamsection_set.all()
                for q in sec:
                    que = q.studentexamquestion_set.all()
                    qu += len(que)
        exams.append(ex)
        questions.append(qu)
    return tests, exams, questions

def DateNum(d):
    data = d.split("/")
    data = data[::-1]
    data = ''.join(data)
    return  int(data)


def Totalpackage_Question_marks(exam):
    tests = []
    exams = []
    questions = []
    marks = []
    ex = 0
    sub = exam.studentpackage_subpackage_set.all()
    for j in sub:
        mrk = []
        qqu = []
        exms = j.sub.studentsubpackage_mainexam_set.all()
        ex += len(exms)
        for k in exms:
            m = 0
            qu = 0
            today = Today()
            exx = StudentMainExam.objects.filter(id=k.main.id).first()
            if exx.status != "Submitted":
                if DateNum(today)>DateNum(k.main.end_date):
                    exx.status = "Expire"
                    exx.save()
                if DateNum(today) < DateNum(k.main.start_date):
                    exx.status = "Wait"
                    exx.save()

            sec = k.main.studentmainexamsection_set.all()
            for q in sec:
                que = q.studentexamquestion_set.all()
                qu += len(que)
                for mr in que:
                    if mr.Question.Type1 and mr.Question.marks1:
                        m += float(mr.Question.marks1)
                    elif mr.Question.Type2 and mr.Question.marks2:
                        m += float(mr.Question.marks2)
                    elif mr.Question.Type3 and mr.Question.marks3:
                        m += float(mr.Question.marks3)
                    elif mr.Question.Type4 and mr.Question.marks4:
                        m += float(mr.Question.marks4)
            mrk.append(m)
            qqu.append(qu)
        marks.append(mrk)
        questions.append(qqu)
    exams.append(ex)
    print(marks, questions)
    return exams, questions, marks


def TotalQuizpackage_Question_marks(student_data, option):
    quiz = []
    if option == "Institute":
        quiz = Assign_Quiz_Institute_Student.objects.filter(student=student_data)
    if option == "External":
        quiz = Assign_Quiz_External_Student.objects.filter(student=student_data)

    questions = []
    marks = []
    for i in quiz:
        que = []
        mmr = []
        sq = i.package.studentquiz_quizpackage_set.all()
        for j in sq:
            m = 0
            qz = j.quiz.studentquiz_questions_set.all()
            que.append(len(qz))
            for mr in qz:
                if mr.Question.Type1 and mr.Question.marks1:
                    m += float(mr.Question.marks1)
                elif mr.Question.Type2 and mr.Question.marks2:
                    m += float(mr.Question.marks2)
                elif mr.Question.Type3 and mr.Question.marks3:
                    m += float(mr.Question.marks3)
                elif mr.Question.Type4 and mr.Question.marks4:
                    m += float(mr.Question.marks4)
            mmr.append(m)
        marks.append(mmr)
        questions.append(que)
    print(marks, questions)
    return marks, questions, quiz






def Dashboard(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    name_split = student_data.name.split(' ')
    l = len(name_split)
    if l>1:
        lname = name_split[1:]
        lname = ' '.join(lname)
    else:
        lname = ''
    name = name_split[0]
    total = 0
    paid = 0
    per = 0
    remain = 0
    per3 = 0
    today_date = date.today()
    Date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    Date = Date.split('/')
    Date = int(''.join(Date[::-1]))

    joined_course = Front_student_course_batch_data.objects.filter(student = student_data)
    option = 'upcoming'
    total_due_fee = 0
    total_upcoming_fee = 0
    for c in joined_course:
        student_fee = Front_student_fee_installment_data.objects.filter(student_course = c)
        for i in student_fee:
            if float(i.remaining_fee) != 0:
                ins_date = i.installment_last_date
                ins_date = ins_date.split('/')
                ins_date = int(''.join(ins_date[::-1]))
                if ins_date < Date:
                    option = 'Due'
                    total_due_fee += float(i.remaining_fee )
                else:
                    total_upcoming_fee += float(i.remaining_fee)
                    break
    total_course = Master_course_data.objects.filter(ins = student_data.ins).count()
    per2 = round((joined_course.count()/total_course)*100)
    noti = Notification_on_panel.objects.filter(student=student_data).order_by('-id')
    doc = Front_document_files.objects.filter(student = student_data).count()
    last_five = noti[:4]
    if user.last_name == "I_Student":
        for i in student_data.front_student_course_batch_data_set.all():
            total = total + int(i.total_fee)
            paid = paid + int(i.total_fee_pay)
            remain = remain + int(i.fee_after_pay)
        per = (paid/total)*100
        per = round(per)
        per3 = round((remain/total)*100)
        per4 = round((total_due_fee/remain)*100)
        per5 = round((total_upcoming_fee / remain) * 100)


    if user.last_name == "I_Student":
        tests, exams, questions = TotalTest_Question(student_data, "Institute")
    if user.last_name == "E_Student":
        tests, exams, questions = TotalTest_Question(student_data, "External")

    context = {"student":student_data,"name":name,"lname":lname,  "ins_data":Institute_data(request.user),
               "per":per,"paid":paid, 'test_series':tests, "exams":exams, "questions":questions,
               "Total":total,"joined_course":joined_course.count(),"total_course":total_course,"per2":per2
               ,"remain":remain,"per3":per3,"noti":noti.count(),"doc":doc,"last_five":last_five,
               "option":option,"upcoming":total_upcoming_fee,"Due":total_due_fee,"per4":per4,"per5":per5}

    return render(request, "StudentHome/dashboard.html",context)

def Chenge_password(request):
    error = False
    if request.method == "POST":
        old = request.POST['old']
        new = request.POST['new']
        user = authenticate(username=request.user.username,password=old)
        if user:
            u = User.objects.filter(username = request.user.username).first()
            u.set_password(new)
            u.save()
            return redirect('StudentPanel:home')
        else:
            error = True
    return render(request,'StudentHome/change_password.html',{"student":Show(request.user),"error":error,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})

def Student_generate_invoice(request,pid):
    user = request.user
    data = Front_student_pay_fee.objects.filter(id = pid).first()
    data22 = Institite_profile.objects.filter().first()
    print("hello python")
    return render(request,'front/front_generate_invoice.html',{"data":data,"data22":data22
                                                               ,"ins_data":Institute_data(user), "adminprofile":Admin_data()})

def AllTests(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)

    if user.last_name == "I_Student":
        tests, exams, questions = TotalTest_Question(student_data, "Institute")
    if user.last_name == "E_Student":
        tests, exams, questions = TotalTest_Question(student_data, "External")

    context = {
        "data":student_data,
        'test_series':tests, "exams":exams, "questions":questions,  "ins_data":Institute_data(request.user)
    }
    return render(request, "StudentHome/Test_Package_List.html", context)



def All_Exams(request, pid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    today = Today()
    exam = StudentExamPackage.objects.filter(id = pid).first()
    exams, questions, marks = Totalpackage_Question_marks(exam)

    context = {
        "exam": exam, "questions": questions, "marks": marks,
        "today":today,  "ins_data":Institute_data(request.user)
    }
    return render(request, "StudentHome/all_test.html", context)


def TestInstruction(request, eid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    exam = StudentMainExam.objects.filter(id = eid).first()
    section = exam.studentmainexamsection_set.first()
    question = section.studentexamquestion_set.first()

    if exam.status == "Submitted":
        return redirect("StudentPanel:analysis", eid)
    if exam.status == "Unseen":
        time = exam.duration
        hour = time.split(":")[0]
        min = time.split(":")[1]
        sec = 0
        qmin = 0
        qsec = 0
    else:
        time = exam.time_remain
        hour = time.split(":")[0]
        min = time.split(":")[1]
        sec = time.split(":")[2]
        last_question = StudentExamQuestion.objects.filter(id=exam.present_question_id).first()
        time = last_question.time_taken
        qmin = time.split(":")[0]
        qsec = time.split(":")[1]

    context = {
        'exam':exam, 'hour':hour, 'min':min, 'sec':sec, 'qmin':qmin, 'qsec':qsec,
        'sid':section.id, 'qid':question.id,  "ins_data":Institute_data(request.user),
        'student':Show(user)
    }
    return render(request, "StudentHome/instruction.html", context)


def LiveTest(request, eid, sid, qid, num, what, time):

    Current_Time = []
    previous, next, pnum, nnum = 0, 0, 0, 0
    section = []
    Questions = []
    section = StudentMainExamSection.objects.filter(id=sid).first()
    question = StudentExamQuestion.objects.filter(id=qid).first()
    if question.status != "Correct" and question.status != "Wrong" :
        question.status = "Seen"
        question.save()

    exam = StudentMainExam.objects.filter(id=eid).first()
    if exam.status == "Submitted":
        return redirect("StudentPanel:analysis", eid)

    for i in section.studentexamquestion_set.all():
        Questions.append(i.id)

    if exam.status == "Unseen":
        exam.status = "Seen"
        exam.time_remain = exam.duration + ":00"
        exam.time_taken = "00:00:00"
        exam.present_question_id = question.id
        exam.save()
        Time = exam.duration
        Current_Time.append(int(Time.split(":")[0]))
        Current_Time.append(Time.split(":")[1])
        Current_Time.append(0)
        Current_Time.append(0)
        Current_Time.append(0)
    else:
        Current_Time = []
        data = time.split("___")
        data.pop(0)
        for i in data:
            Current_Time.append(i.split("t1AZ4uvq")[0])
        print(Current_Time)
        exam.time_remain = Current_Time[0] + ":" + Current_Time[1] + ":" + Current_Time[2]

        Time = exam.duration
        thour = int(Time.split(":")[0]) - int(Current_Time[0])
        tmin = int(Time.split(":")[1]) - int(Current_Time[1])
        tsec = int(Current_Time[2])
        exam.time_taken = str(thour) + ":" + str(tmin) + ":" + str(tsec)

        last_question = StudentExamQuestion.objects.filter(id=exam.present_question_id).first()
        last_question.time_taken = Current_Time[3] + ":" + Current_Time[4]
        last_question.save()

        if exam.present_question_id == qid:
            question.time_taken = Current_Time[3] + ":" + Current_Time[4]
            question.save()

        exam.present_question_id = qid
        exam.save()

        Current_Time.pop(4)
        Current_Time.pop(3)

        Time = question.time_taken
        Current_Time.append(int(Time.split(":")[0]))
        Current_Time.append(Time.split(":")[1])


    prqindex = Questions.index(question.id)
    if prqindex == 0:
        previous = question.id
        pnum = num
    else:
        previous = Questions[prqindex-1]
        pnum = int(num)-1
    if Questions[prqindex] == Questions[-1]:
        next = question.id
        nnum = num
    else:
        next = Questions[prqindex+1]
        nnum = int(num)+1

    sec_com = []
    Answered = []
    Not_Ans = []
    Review = []
    Not_Visited = []
    for sec in exam.studentmainexamsection_set.all():
        que = StudentExamQuestion.objects.filter(MainSection = sec)
        n, na, nv, re = 0, 0, 0, 0
        for i in que:
            if i.status == "Correct" or i.status == "Wrong":
                n += 1
            if i.status == "Seen":
                na += 1
            if i.status == "Unseen":
                nv += 1
            if i.status2 == "Tag":
                re += 1
        Answered.append(n)
        Not_Ans.append(na)
        Review.append(re)
        Not_Visited.append(nv)
        per = round((n*100)/len(que))
        sec_com.append(per)

    if request.method == "POST":
        question.status2 = "UnTag"
        if question.Question.Type1:
            ans = request.POST["T1ans"]
            if ans != '0':
                question.Type1Ans = ans
                if question.Question.TrueAns == ans:
                    print("Correct")
                    question.status = "Correct"
                else:
                    print("Wrong")
                    question.status = "Wrong"

            else:
                question.Type1Ans = '0'
                question.status = "Seen"
            question.save()

        if question.Question.Type2:
            true = []
            if question.Question.Answer1:
                true.append(1)
            if question.Question.Answer2:
                true.append(1)
            if question.Question.Answer3:
                true.append(1)
            if question.Question.Answer4:
                true.append(1)

            ans = request.POST.getlist("Type2ans")
            print(ans)
            if ans:
                question.Type2Ans1 = False
                question.Type2Ans2 = False
                question.Type2Ans3 = False
                question.Type2Ans4 = False
                question.save()
                you = "Wrong"
                for i in ans:
                    if i == '1':
                        question.Type2Ans1 = True
                        if question.Question.Answer1 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '2':
                        question.Type2Ans2 = True
                        if question.Question.Answer2 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '3':
                        question.Type2Ans3 = True
                        if question.Question.Answer3 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '4':
                        question.Type2Ans4 = True
                        if question.Question.Answer4 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                question.status = you

            else:
                question.Type2Ans1 = False
                question.Type2Ans2 = False
                question.Type2Ans3 = False
                question.Type2Ans4 = False
                question.status = "Seen"
            question.save()
        if question.Question.Type3:
            ans = request.POST["Type3ans"]
            Lans = ans.lower()
            Uans = ans.upper()
            if ans:
                if ans == question.Question.Answer31 or ans == question.Question.Answer32 \
                    or Lans == question.Question.Answer31 or Lans == question.Question.Answer32 \
                    or Uans == question.Question.Answer31 or Uans == question.Question.Answer32:
                    question.status = "Correct"
                else:
                    question.status = "Wrong"
                question.Type3Ans1 = ans
                question.save()
            else:
                question.save()

        if question.Question.Type4:
            ans = request.POST["Type4ans"]
            if ans != '0':
                if ans == question.Question.TrueAns1:
                    question.status = "Correct"
                else:
                    question.status = "Wrong"
                question.Type4Ans = ans
                question.save()
            else:
                question.Type4Ans = '0'
                question.status = "Seen"
                question.save()

        return redirect("StudentPanel:live", eid, sid, qid, num, "Live", time)
    print(sec_com)
    context = {
        'exam': exam, 'section':section, 'question':question, 'exam':exam, 'sec_com':sec_com,  "ins_data":Institute_data(request.user),
        'hour':Current_Time[0], 'pnum':pnum, 'nnum':nnum,'pre':previous, 'next':next,
        'min':Current_Time[1], 'sec':Current_Time[2], 'Answered':Answered, 'Not_Ans':Not_Ans,
                   'Review':Review, 'Not_Visited':Not_Visited, 'iqid':int(qid),
         'eid':eid, 'sid':sid, 'qid':qid, 'num':num, 'qmin':Current_Time[3], 'qsec':Current_Time[4],
    }

    if what == "Tag":
        question.status2 = "Tag"
        question.save()
        return redirect("StudentPanel:live", eid, sid, qid, num, "Live", time)
    if what == "Live":
        return render(request, "StudentHome/live_test.html", context)
    if what == "Instruction":
        return render(request, "StudentHome/live_test_instruction.html", context)
    if what == "Question":
        return render(request, "StudentHome/live_test_questions.html", context)


def YourRank(exam):
    Mainexam = MainExam.objects.filter(id = exam.main.id).first()
    Assign_Exams = Mainexam.studentmainexam_set.all()
    marks = []
    for exam in Assign_Exams:
        if exam.status == "Submitted":
            true = 0
            false = 0
            true_attempt = 0
            attempt = 0
            total = 0
            total_marks = 0
            for sec in exam.studentmainexamsection_set.all():
                que = StudentExamQuestion.objects.filter(MainSection=sec)
                total += len(que)
                for i in que:
                    t = 0
                    f = 0
                    if i.Question.Type1:
                        t = i.Question.marks1
                        f = i.Question.minus1
                    elif i.Question.Type2:
                        t = i.Question.marks2
                        f = i.Question.minus2
                    elif i.Question.Type3:
                        t = i.Question.marks3
                        f = i.Question.minus3
                    elif i.Question.Type4:
                        t = i.Question.marks4
                        f = i.Question.minus4
                    if t:
                        total_marks += float(t)

                    if i.status == "Correct":
                        true += float(t)
                        attempt += 1
                        true_attempt += 1
                    if i.status == "Seen" or i.status == "Unseen":
                        pass
                    if i.status == "Wrong":
                        false += float(f)
                        attempt += 1
            your_marks = true - false
            marks.append(float("{0:.2f}".format(your_marks)))
    marks = list(set(marks))
    marks.sort(reverse=True)
    return marks


def YourMarks(exam):
    true = 0
    false = 0
    true_attempt = 0
    attempt = 0
    total = 0
    total_marks = 0
    sec_marks = []
    your_sec_question = []
    sec_accuracy = []
    for sec in exam.studentmainexamsection_set.all():
        ua = 0
        sm = 0
        ust = 0
        usf = 0
        t_a = 0
        que = StudentExamQuestion.objects.filter(MainSection=sec)
        total += len(que)
        for i in que:
            t = 0
            f = 0
            if i.Question.Type1:
                t = i.Question.marks1
                f = i.Question.minus1
            elif i.Question.Type2:
                t = i.Question.marks2
                f = i.Question.minus2
            elif i.Question.Type3:
                t = i.Question.marks3
                f = i.Question.minus3
            elif i.Question.Type4:
                t = i.Question.marks4
                f = i.Question.minus4
            if t:
                total_marks += float(t)
                sm += float(t)

            if i.status == "Correct":
                true += float(t)
                ust += float(t)
                attempt += 1
                true_attempt += 1
                t_a += 1
                ua += 1
            if i.status == "Seen" or i.status == "Unseen":
                pass
            if i.status == "Wrong":
                false += float(f)
                usf += float(f)
                attempt += 1
                ua += 1
        ysm = float("{0:.2f}".format(ust-usf))
        your_sec_question.append(ua)
        sec_marks.append([sm, ysm])
        if ua>0:
            sec_accuracy.append(float("{0:.2f}".format((t_a * 100) / ua)))
        else:
            sec_accuracy.append(0.0)


    your_marks = true - false
    All_Marks = YourRank(exam)
    your_rank = All_Marks.index(float("{0:.2f}".format(your_marks))) + 1
    print(your_rank)
    accuracy = 0
    if attempt > 0:
        accuracy = (true_attempt * 100) / attempt

    accuracy = float("{0:.2f}".format(accuracy))
    exam.your_marks = float("{0:.2f}".format(your_marks))
    exam.accuracy = accuracy
    exam.attempt = attempt
    exam.save()
    Top10 = 0

    if len(All_Marks) > 10:
        Top10 = All_Marks[:10]
    else:
        Top10 = All_Marks
    Topper_Students = []
    for i in Top10:
        da = StudentMainExam.objects.filter(your_marks = i)
        for j in da:
            Topper_Students.append(j)

    return accuracy, total_marks, total, your_rank, All_Marks, Topper_Students, sec_marks, your_sec_question, sec_accuracy



def Next_Test_Series(exam):
    tests = []
    exams = []
    questions = []
    marks = []
    ex = 0
    sub = exam.studentpackage_subpackage_set.all()
    for j in sub:
        mrk = []
        qqu = []
        exms = j.sub.studentsubpackage_mainexam_set.all()
        ex += len(exms)
        for k in exms:
            m = 0
            qu = 0
            sec = k.main.studentmainexamsection_set.all()
            for q in sec:
                que = q.studentexamquestion_set.all()
                qu += len(que)
                for mr in que:
                    if mr.Question.Type1 and mr.Question.marks1:
                        m += float(mr.Question.marks1)
                    elif mr.Question.Type2 and mr.Question.marks2:
                        m += float(mr.Question.marks2)
                    elif mr.Question.Type3 and mr.Question.marks3:
                        m += float(mr.Question.marks3)
                    elif mr.Question.Type4 and mr.Question.marks4:
                        m += float(mr.Question.marks4)
            mrk.append(m)
            qqu.append(qu)
        marks.append(mrk)
        questions.append(qqu)
    exams.append(ex)
    print(marks, questions)
    return exams, questions, marks




def TestAnalysis(request, eid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student = Show(user)
    name = student.name.split()[0]

    exam = StudentMainExam.objects.filter(id=eid).first()
    section = exam.studentmainexamsection_set.first()
    question = section.studentexamquestion_set.first()
    if exam.status == "Seen":
        exam.status = "Submitted"
        exam.date = Today()
        exam.save()
    accuracy, total_marks, total, your_rank, All_Marks, Topper_Students, sec_marks, your_sec_question, sec_accuracy  = YourMarks(exam)
    if exam.IStudent:
        student = Front_student_data.objects.filter(id = exam.IStudent.id).first()
        exams = student.studentmainexam_set.all()
        Exams = []
        Questions = []
        Total_Marks = []
        nn = 0
        for i in exams:
            if i.status != "Submitted":
                nn += 1
                Exams.append(i)
                m = 0
                qu = 0
                sec = i.studentmainexamsection_set.all()
                for q in sec:
                    que = q.studentexamquestion_set.all()
                    qu += len(que)
                    for mr in que:
                        if mr.Question.Type1 and mr.Question.marks1:
                            m += float(mr.Question.marks1)
                        elif mr.Question.Type2 and mr.Question.marks2:
                            m += float(mr.Question.marks2)
                        elif mr.Question.Type3 and mr.Question.marks3:
                            m += float(mr.Question.marks3)
                        elif mr.Question.Type4 and mr.Question.marks4:
                            m += float(mr.Question.marks4)
                Total_Marks.append(m)
                Questions.append(qu)
                if nn >= 3:
                    break
    if exam.EStudent:
        student = Add_New_Student.objects.filter(id = exam.EStudent.id).first()
        exams = student.studentmainexam_set.all()
        Exams = []
        Questions = []
        Total_Marks = []
        nn = 0
        for i in exams:
            if i.status != "Submitted":
                nn += 1
                Exams.append(i)
                m = 0
                qu = 0
                sec = i.studentmainexamsection_set.all()
                for q in sec:
                    que = q.studentexamquestion_set.all()
                    qu += len(que)
                    for mr in que:
                        if mr.Question.Type1 and mr.Question.marks1:
                            m += float(mr.Question.marks1)
                        elif mr.Question.Type2 and mr.Question.marks2:
                            m += float(mr.Question.marks2)
                        elif mr.Question.Type3 and mr.Question.marks3:
                            m += float(mr.Question.marks3)
                        elif mr.Question.Type4 and mr.Question.marks4:
                            m += float(mr.Question.marks4)
                Total_Marks.append(m)
                Questions.append(qu)
                if nn >= 3:
                    break

    context = {
        'exam':exam, 'section':section, 'question':question, 'accuracy':exam.accuracy, "your_marks":exam.your_marks, "total_marks":total_marks, 'Exams':Exams, "Que":Questions, "Marks":Total_Marks,
        'total':total, 'attempt':exam.attempt, "your_rank":your_rank, "All_Marks":len(All_Marks),  "ins_data":Institute_data(request.user), 'name':name,
        "Toppers":Topper_Students, "sec_marks":sec_marks, "your_sec_question":your_sec_question, "sec_accuracy":sec_accuracy
    }
    print(Topper_Students)

    return render(request, "StudentHome/test_analysis.html", context)



def Practice(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    packages = Assign_Study_Institute_Student.objects.filter(student = student_data)
    return render(request, "StudentHome/practice.html", {"packages":packages,  "ins_data":Institute_data(request.user)})



def PracticeQuestion(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    return render(request, "StudentHome/practice_questions.html", { "ins_data":Institute_data(request.user)})

def StartPractice(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    return render(request, "StudentHome/single_question.html", { "ins_data":Institute_data(request.user)})





def AllQuiz(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    if user.last_name == "I_Student":
        marks, questions, quiz = TotalQuizpackage_Question_marks(student_data, "Institute")
    if user.last_name == "E_Student":
        marks, questions, quiz = TotalQuizpackage_Question_marks(student_data, "External")

    context = {
        "marks":marks, "questions":questions, "quiz":quiz,  "ins_data":Institute_data(request.user)
    }
    return render(request, "StudentHome/quiz.html", context)



def StartQuiz(request, qid, q_id, time):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")


    quiz = StudentQuiz.objects.filter(id=qid).first()
    if quiz.status == "Submitted":
        return redirect("StudentPanel:quiz_summery", quiz.id)

    Questions = []
    if quiz.status == "Unseen":
        quiz.status = "Seen"
        quiz.time_remain = quiz.duration + ":00"
        quiz.time_taken = "00:00"
        quiz.save()
        return redirect("StudentPanel:start_quiz", qid, q_id, time)


    min = 0
    sec = 0
    if time == '0':
        time = quiz.time_remain
        time = time.split(":")
        min = int(time[0])
        sec = int(time[1])
    else:
        Current_Time = []
        data = time.split("___")
        data.pop(0)
        for i in data:
            Current_Time.append(i.split("t1AZ4uvq")[0])
        min = int(Current_Time[0])
        sec = int(Current_Time[1])
        if min and sec:
            quiz.time_remain = str(min) + ":" + str(sec)
            quiz.time_taken = str((int(quiz.duration) - int(min))) + ":" + str(sec)
            quiz.save()

    if q_id == "0":
        question = quiz.studentquiz_questions_set.first()
    else:
        question = StudentQuiz_Questions.objects.filter(id = q_id).first()
    if question.status != "Correct" and question.status != "Wrong":
        question.status = "Seen"
        question.save()

    for i in quiz.studentquiz_questions_set.all():
        Questions.append(i.id)

    print(Questions)
    prqindex = Questions.index(question.id)
    if prqindex == 0:
        previous = question.id
    else:
        previous = Questions[prqindex - 1]

    if Questions[prqindex] == Questions[-1]:
        next = question.id
    else:
        next = Questions[prqindex + 1]

    num = Questions.index(question.id) + 1


    answered = len(StudentQuiz_Questions.objects.filter(quiz = quiz,status = "Correct"))
    answered += len(StudentQuiz_Questions.objects.filter(quiz = quiz,status = "Wrong"))
    not_answered = len(StudentQuiz_Questions.objects.filter(quiz = quiz,status = "Seen"))
    skiped = len(StudentQuiz_Questions.objects.filter(quiz = quiz,status = "Unseen"))


    if request.method == "POST":
        min = request.POST['min']
        sec = request.POST['sec']

        if min and sec:
            quiz.time_remain = min + ":" + sec
            print(min, sec)
            quiz.time_taken = str((int(quiz.duration) - int(min))) + ":" + sec
            quiz.save()

        if question.Question.Type1:
            ans = request.POST["T1ans"]
            if ans != '0':
                question.Type1Ans = ans
                if question.Question.TrueAns == ans:
                    print("Correct")
                    question.status = "Correct"
                else:
                    print("Wrong")
                    question.status = "Wrong"

            else:
                question.Type1Ans = '0'
                question.status = "Seen"
            question.save()

        if question.Question.Type2:
            true = []
            if question.Question.Answer1:
                true.append(1)
            if question.Question.Answer2:
                true.append(1)
            if question.Question.Answer3:
                true.append(1)
            if question.Question.Answer4:
                true.append(1)

            ans = request.POST.getlist("Type2ans")
            print(ans)
            if ans:
                question.Type2Ans1 = False
                question.Type2Ans2 = False
                question.Type2Ans3 = False
                question.Type2Ans4 = False
                question.save()
                you = "Wrong"
                for i in ans:
                    if i == '1':
                        question.Type2Ans1 = True
                        if question.Question.Answer1 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '2':
                        question.Type2Ans2 = True
                        if question.Question.Answer2 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '3':
                        question.Type2Ans3 = True
                        if question.Question.Answer3 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                    if i == '4':
                        question.Type2Ans4 = True
                        if question.Question.Answer4 and len(true) == len(ans):
                            you = "Correct"
                        else:
                            you = "Wrong"
                question.status = you

            else:
                question.Type2Ans1 = False
                question.Type2Ans2 = False
                question.Type2Ans3 = False
                question.Type2Ans4 = False
                question.status = "Seen"
            question.save()
        if question.Question.Type3:
            ans = request.POST["Type3ans"]
            Lans = ans.lower()
            Uans = ans.upper()
            if ans:
                if ans == question.Question.Answer31 or ans == question.Question.Answer32 \
                        or Lans == question.Question.Answer31 or Lans == question.Question.Answer32 \
                        or Uans == question.Question.Answer31 or Uans == question.Question.Answer32:
                    question.status = "Correct"
                else:
                    question.status = "Wrong"
                question.Type3Ans1 = ans
                question.save()
            else:
                question.save()

        if question.Question.Type4:
            ans = request.POST["Type4ans"]
            if ans != '0':
                if ans == question.Question.TrueAns1:
                    question.status = "Correct"
                else:
                    question.status = "Wrong"
                question.Type4Ans = ans
                question.save()
            else:
                question.Type4Ans = '0'
                question.status = "Seen"
                question.save()

        return redirect("StudentPanel:start_quiz", qid, q_id, time)

    context = { 'pre':previous, 'next':next, 'qid':qid, 'min':min, 'sec':sec, 'q_id':q_id,
        "ins_data":Institute_data(request.user), "question": question, 'quiz':quiz, 'num':num,
                'answered': answered, 'not_answered': not_answered, 'skiped': skiped
                }
    return render(request, "StudentHome/start_quiz.html", context)





def YourQuizMarks(quiz):
    true = 0
    false = 0
    for i in quiz.studentquiz_questions_set.all():
        t = 0
        f = 0
        if i.Question.Type1:
            t = i.Question.marks1
            f = i.Question.minus1
        elif i.Question.Type2:
            t = i.Question.marks2
            f = i.Question.minus2
        elif i.Question.Type3:
            t = i.Question.marks3
            f = i.Question.minus3
        elif i.Question.Type4:
            t = i.Question.marks4
            f = i.Question.minus4

        if i.status == "Correct":
            true += float(t)
        if i.status == "Seen" or i.status == "Unseen":
            pass
        if i.status == "Wrong":
            false += float(f)
    your = float("{0:.2f}".format(true-false))
    return your

def YourQuizRank(quiz):
    Mainquiz = Quiz.objects.filter(id = quiz.main.id).first()
    Assigned_Quizes = Mainquiz.studentquiz_set.all()
    marrks = []
    for i in Assigned_Quizes:
        if i.status == "Submitted":
            marrks.append(float(i.your_marks))
    marrks.sort(reverse=True)
    marrks = set(marrks)
    marrks = list(marrks)
    rank = marrks.index(float(i.your_marks)) + 1
    return str(rank) + "/" + str(len(marrks))




def QuizSummery(request, qid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student = Show(user)
    name = student.name.split()[0]

    quiz = StudentQuiz.objects.filter(id=qid).first()
    if quiz.status != "Submitted":
        quiz.status = "Submitted"
        quiz.your_marks = YourQuizMarks(quiz)
        quiz.date = Today()
        quiz.save()

    correct = len(StudentQuiz_Questions.objects.filter(quiz=quiz, status="Correct"))
    incorrect = len(StudentQuiz_Questions.objects.filter(quiz=quiz, status="Wrong"))
    not_answered = len(StudentQuiz_Questions.objects.filter(quiz=quiz, status="Seen"))
    not_answered += len(StudentQuiz_Questions.objects.filter(quiz=quiz, status="Unseen"))
    context = {
        "quiz":quiz, 'correct':correct, 'incorrect':incorrect,
        'not_answered':not_answered, "ins_data":Institute_data(request.user),
        "rank":YourQuizRank(quiz), 'name':name
    }
    return render(request, "StudentHome/quiz_summery.html", context)


def QuizSolution(request, qid, q_id):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    Questions = []
    quiz = StudentQuiz.objects.filter(id = qid).first()

    if q_id == "0":
        question = quiz.studentquiz_questions_set.first()
    else:
        question = StudentQuiz_Questions.objects.filter(id = q_id).first()


    for i in quiz.studentquiz_questions_set.all():
        Questions.append(i.id)

    print(Questions)
    prqindex = Questions.index(question.id)
    if prqindex == 0:
        previous = question.id
    else:
        previous = Questions[prqindex - 1]

    if Questions[prqindex] == Questions[-1]:
        next = question.id
    else:
        next = Questions[prqindex + 1]

    num = Questions.index(question.id) + 1

    context = { 'pre':previous, 'next':next, 'qid':qid,
        "ins_data":Institute_data(request.user), "question": question, 'quiz':quiz, 'num':num
                }
    return render(request, "StudentHome/quiz_solution.html", context)




import os
def Study_Material(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    data = []
    extension = []
    for i in student_data.front_student_course_batch_data_set.all():
        batch = Master_batch_data.objects.filter(id = i.Batch.id).first()
        material = Material_Batch.objects.filter(batch = batch)
        for m in material:
            study = StudyMaterial.objects.filter(id = m.material.id).first()
            fileName, fileExtension = os.path.splitext(study.file.name)
            data.append(study)
            extension.append(fileExtension)
    return render(request, "StudentHome/studyMaterial.html", {"data":data, 'extension':extension,  "ins_data":Institute_data(request.user)})


##################### Running Batch Function in diffrent way ###############
def Running_batch_check2(d, u):
    student = Front_student_data.objects.filter(usr = u).first()
    running_batch = []
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    Tdate = int(''.join(date_reverse))

    if d == 0:
        all_batch = Master_batch_data.objects.filter(ins = student.ins)
    else:
        course = Master_course_data.objects.filter(id = d).first()
        all_batch = Master_batch_data.objects.filter(ins = student.ins, course = course)
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



###########################################################################
###########Courses############
def Courses(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    li=[]
    student_data = Show(user)

    for i in student_data.front_student_course_batch_data_set.all():
        cc = i.course.id
        rn_batch = Running_batch_check2(cc,user)
        batch = Master_batch_data.objects.filter(id = i.Batch.id).first()
        if batch in rn_batch:
            li.append(batch.id)


    return render(request, "StudentHome/Courses.html",{"student":student_data,"li":li,  "ins_data":Institute_data(request.user)})

def FeeDetails(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    li = []
    student_data = Show(user)

    for i in student_data.front_student_course_batch_data_set.all():
        cc = i.course.id
        rn_batch = Running_batch_check2(cc,user)
        batch = Master_batch_data.objects.filter(id = i.Batch.id).first()
        if batch in rn_batch:
            li.append(batch.id)
    context = {"student":student_data,"li":li, "ins_data":Institute_data(request.user)}
    return render(request, "StudentHome/fee.html",context)

def FeeInstallmentDetails(request,cid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    data = Front_student_course_batch_data.objects.filter(id = cid).first()
    return render(request,'StudentHome/installment_details.html',{"data":data,"student":Show(user),  "ins_data":Institute_data(request.user)})

def Invoice(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    return render(request, "StudentHome/invoice.html")

def Student_Notifications(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data =Show(user)
    all_notification = student_data.notification_on_panel_set.order_by('-id')

    return render(request,'StudentHome/student_notification.html',{"student":student_data,
                                                                   "all_notification":all_notification,  "ins_data":Institute_data(request.user)})

def Student_Upload_Documents(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    all_doc = student_data.front_document_files_set.all().order_by('-id')

    return render(request,'StudentHome/student_uploaded_document.html',{"student":student_data,  "ins_data":Institute_data(request.user),
                                                                        "all_doc":all_doc})

def Student_Ecorner(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data =Show(user)
    online_books = Master_E_Book.objects.filter(ins = student_data.ins).order_by('-id')

    return render(request,'StudentHome/student_ecorner.html',{"student":student_data,"online_book":online_books,  "ins_data":Institute_data(request.user)})

def Student_issued_returned_book(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student_data = Show(user)
    books = Library_Issue_Book.objects.filter(student = student_data)
    return render(request,'StudentHome/student_i_r_book.html',{"student":student_data,"books":books,  "ins_data":Institute_data(request.user)})

########## Add Link Function #########
def Students_Link_add(request,option):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    if request.method == "POST":
        d = request.POST
        sdata = Show(user)
        data = Student_add_link.objects.filter(student = sdata).first()
        if data:
            if option == 'Twitter':
                data.twitter_link = d['Twitter']
                data.save()
            if option == 'Facebook':
                data.facebook_link = d['Facebook']
                data.save()
            if option == 'Instagram':
                data.instagram_link = d['Instagram']
                data.save()

        else:
            if option == 'Twitter':
                t = d['Twitter']
                Student_add_link.objects.create(student = sdata,twitter_link =t )
            if option == 'Facebook':
                f = d['Facebook']
                Student_add_link.objects.create(student=sdata, twitter_link=f)
            if option == 'Instagram':
                i = d['Instagram']
                Student_add_link.objects.create(student=sdata, twitter_link=i)

        return redirect('StudentPanel:home')


def Student_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student = Show(user)
    return render(request,'StudentHome/profile.html',{"student":student,  "ins_data":Institute_data(request.user)})


def Student_edit_profile(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    student = Show(user)
    if request.method == "POST":
        d = request.POST
        dob = d['dob']
        mobile = d['mob']
        email = d['email']
        address = d['address']
        gender = d['gender']
        college = d['college']
        graduation = d['graduation']
        stream = d['stream']
        fname = d['fname']
        fadd = d['fadd']
        fmob = d['fmob']
        o = d['occupation']
        student.dob = dob
        student.mobile = mobile
        student.email = email
        student.address = address
        student.gender = gender
        student.college = college
        student.graduation = graduation
        student.stream = stream
        student.Father_name = fname
        student.father_add = fadd
        student.father_mob = fmob
        student.Occupation = o
        student.save()

        return redirect('StudentPanel:home')
    return render(request,'StudentHome/student_edit_profile.html',{"student":student,  "ins_data":Institute_data(request.user)})



def ExamSolution(request, eid, sid, qid, num, what, time):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_student(user):
        return redirect("login")

    Current_Time = [0, 0, 0, 0 ,0]

    Questions = []
    section = StudentMainExamSection.objects.filter(id=sid).first()
    question = StudentExamQuestion.objects.filter(id=qid).first()
    exam = StudentMainExam.objects.filter(id=eid).first()
    if exam.status != "Submitted":
        print("Hello")
        return redirect("StudentPanel:analysis", eid)

    for i in section.studentexamquestion_set.all():
        Questions.append(i.id)

    prqindex = Questions.index(question.id)
    if prqindex == 0:
        previous = question.id
        pnum = num
    else:
        previous = Questions[prqindex - 1]
        pnum = int(num) - 1
    if Questions[prqindex] == Questions[-1]:
        next = question.id
        nnum = num
    else:
        next = Questions[prqindex + 1]
        nnum = int(num) + 1

    sec_com = []
    Answered = []
    Not_Ans = []
    Review = []
    Not_Visited = []
    for sec in exam.studentmainexamsection_set.all():
        que = StudentExamQuestion.objects.filter(MainSection = sec)
        n, na, nv, re = 0, 0, 0, 0
        for i in que:
            if i.status == "Correct" or i.status == "Wrong":
                n += 1
            if i.status == "Seen":
                na += 1
            if i.status == "Unseen":
                nv += 1
            if i.status2 == "Tag":
                re += 1
        Answered.append(n)
        Not_Ans.append(na)
        Review.append(re)
        Not_Visited.append(nv)
        per = round((n*100)/len(que))
        sec_com.append(per)

    context = {
        'exam': exam, 'section': section, 'question': question, 'exam': exam,
        'hour': Current_Time[0], 'pnum': pnum, 'nnum': nnum, 'pre': previous, 'next': next,
        'min': Current_Time[1], 'sec': Current_Time[2], 'student': Show(user),
         'iqid': int(qid), 'sec_com':sec_com,
        'student': Show(user), 'eid': eid, 'sid': sid, 'qid': qid, 'num': num, 'qmin': Current_Time[3],
        'qsec': Current_Time[4],  "ins_data":Institute_data(request.user)
    }

    return render(request, "StudentHome/analysis_test_questions.html", context)






