from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from Institute.models import *
from Frontdesk.models import *
from WebSite.models import *
class ExamPackage(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True)
    o_fee = models.CharField(max_length=10, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    syllabus = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=150, default="UnPublish")

    def __str__(self):
        return self.name + "------" + self.course.name



class ExamSubPackage(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Package_Subpackage(models.Model):
    package = models.ForeignKey(ExamPackage, on_delete=models.CASCADE, null=True)
    sub = models.ForeignKey(ExamSubPackage, on_delete=models.CASCADE, null=True)



class MainExam(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    instruction = RichTextUploadingField(blank=True, null=True)
    syllabus = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class SubPackage_MainExam(models.Model):
    sub = models.ForeignKey(ExamSubPackage, on_delete=models.CASCADE, null=True)
    main = models.ForeignKey(MainExam, on_delete=models.CASCADE, null=True)



class MainExamSection(models.Model):
    exam = models.ForeignKey(MainExam, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


Ans = [
    ['1', '1'],
    ['2', '2'],
    ['3', '3'],
    ['4', '4'],
]


Ans1 = [
    ['0', 'Select'],
    ['1', 'True'],
    ['2', 'False']
]

class Question_Section(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)


class MultipleChoiceQuestions(models.Model):
    section = models.ForeignKey(Question_Section, on_delete=models.SET_NULL, null=True)
    Type1 = models.BooleanField(default=False)
    Questions = RichTextUploadingField(blank=True, null=True)
    Option_1 = RichTextUploadingField(blank=True, null=True)
    Option_2 = RichTextUploadingField(blank=True, null=True)
    Option_3 = RichTextUploadingField(blank=True, null=True)
    Option_4 = RichTextUploadingField(blank=True, null=True)
    TrueAns = models.CharField(max_length=5, choices=Ans, default='1', null=True)
    marks1 = models.CharField(max_length=5, null=True, blank=True)
    minus1 = models.CharField(max_length=20, null=True)
    explain1 = RichTextUploadingField(blank=True, null=True)

    Type2 = models.BooleanField(default=False)
    Question = RichTextUploadingField(blank=True, null=True)
    Option1 = RichTextUploadingField(blank=True, null=True)
    Option2 = RichTextUploadingField(blank=True, null=True)
    Option3 = RichTextUploadingField(blank=True, null=True)
    Option4 = RichTextUploadingField(blank=True, null=True)
    Answer1 = models.BooleanField(default=False)
    Answer2 = models.BooleanField(default=False)
    Answer3 = models.BooleanField(default=False)
    Answer4 = models.BooleanField(default=False)
    marks2 = models.CharField(max_length=5, null=True, blank=True)
    minus2 = models.CharField(max_length=20, null=True)
    explain2 = RichTextUploadingField(blank=True, null=True)

    Type3 = models.BooleanField(default=False)
    Que = RichTextUploadingField(blank=True, null=True)
    Answer31 = models.CharField(max_length=250, null=True, blank=True)
    Answer32 = models.CharField(max_length=250, null=True, blank=True)
    marks3 = models.CharField(max_length=5, null=True, blank=True)
    minus3 = models.CharField(max_length=20, null=True)
    explain3 = RichTextUploadingField(blank=True, null=True)

    Type4 = models.BooleanField(default=False)
    Ques_tion = RichTextUploadingField(blank=True, null=True)
    TrueAns1 = models.CharField(max_length=5, choices=Ans1, default='0')
    marks4 = models.CharField(max_length=5, null=True, blank=True)
    minus4 = models.CharField(max_length=20, null=True)
    explain4 = RichTextUploadingField(blank=True, null=True)



class ExamQuestion(models.Model):
    MainSection = models.ForeignKey(MainExamSection, on_delete=models.CASCADE)
    Question = models.ForeignKey(MultipleChoiceQuestions, on_delete=models.CASCADE)

    def __str__(self):
        return self.Question.Questions



class QuizPackage(models.Model):
    course = models.ForeignKey(Sub_course, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True, default=0)
    o_fee = models.CharField(max_length=10, null=True, blank=True, default=0)
    syllabus = models.FileField(null=True, blank=True)
    status = models.CharField(max_length=150, default="UnPublish")


class Quiz(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name


class Quiz_QuizPackage(models.Model):
    package = models.ForeignKey(QuizPackage, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class Quiz_Questions(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    Question = models.ForeignKey(MultipleChoiceQuestions, on_delete=models.CASCADE)



class DailyPracticeSubject(models.Model):
    course = models.ForeignKey(Sub_course, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name + " / Course:" + self.course.name


class Topic(models.Model):
    package = models.ForeignKey(DailyPracticeSubject, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)



class Topic_Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    Question = models.ForeignKey(MultipleChoiceQuestions, on_delete=models.CASCADE, null=True)



class StudyMaterial(models.Model):
    course = models.ForeignKey(Master_course_data, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    date = models.CharField(max_length=250, null=True, blank=True)
    file = models.FileField(null=True, blank=True)


class Material_Batch(models.Model):
    batch = models.ForeignKey(Master_batch_data, on_delete=models.CASCADE, null=True)
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE, null=True)

Gender = [
    ['Male', 'Male'],
    ['Female', 'Female']
]


class StudentQuestions(models.Model):
    section = models.ForeignKey(Question_Section, on_delete=models.SET_NULL, null=True)
    Type1 = models.BooleanField(default=False)
    Questions = RichTextUploadingField(blank=True, null=True)
    Option_1 = RichTextUploadingField(blank=True, null=True)
    Option_2 = RichTextUploadingField(blank=True, null=True)
    Option_3 = RichTextUploadingField(blank=True, null=True)
    Option_4 = RichTextUploadingField(blank=True, null=True)
    TrueAns = models.CharField(max_length=5, choices=Ans, default='1', null=True, blank=True)
    marks1 = models.CharField(max_length=5, null=True, blank=True)
    minus1 = models.CharField(max_length=20, null=True)
    explain1 = RichTextUploadingField(blank=True, null=True)

    Type2 = models.BooleanField(default=False)
    Question = RichTextUploadingField(blank=True, null=True)
    Option1 = RichTextUploadingField(blank=True, null=True)
    Option2 = RichTextUploadingField(blank=True, null=True)
    Option3 = RichTextUploadingField(blank=True, null=True)
    Option4 = RichTextUploadingField(blank=True, null=True)
    Answer1 = models.BooleanField(default=False)
    Answer2 = models.BooleanField(default=False)
    Answer3 = models.BooleanField(default=False)
    Answer4 = models.BooleanField(default=False)
    marks2 = models.CharField(max_length=5, null=True, blank=True)
    minus2 = models.CharField(max_length=20, null=True, blank=True)
    explain2 = RichTextUploadingField(blank=True, null=True)

    Type3 = models.BooleanField(default=False)
    Que = RichTextUploadingField(blank=True, null=True)
    Answer31 = models.CharField(max_length=250, null=True, blank=True)
    Answer32 = models.CharField(max_length=250, null=True, blank=True)
    marks3 = models.CharField(max_length=5, null=True, blank=True)
    minus3 = models.CharField(max_length=20, null=True)
    explain3 = RichTextUploadingField(blank=True, null=True)

    Type4 = models.BooleanField(default=False)
    Ques_tion = RichTextUploadingField(blank=True, null=True)
    TrueAns1 = models.CharField(max_length=5, choices=Ans1, default='0')
    marks4 = models.CharField(max_length=5, null=True, blank=True)
    minus4 = models.CharField(max_length=20, null=True)
    explain4 = RichTextUploadingField(blank=True, null=True)

class Add_New_Student(models.Model):
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    dob = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=150, choices=Gender)
    mobile = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    id_proof = models.FileField(null=True, blank=True)
    college = models.CharField(max_length=150, null=True, blank=True)
    pursuing = models.CharField(max_length=150,  null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)



''' ******* Student Assign Exam Package MoDEL ******'''
class StudentExamPackage(models.Model):
    course = models.ForeignKey(Sub_course, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True)
    o_fee = models.CharField(max_length=10, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    syllabus = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name + "------" + self.course.name


class StudentExamSubPackage(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    syllabus = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class StudentPackage_Subpackage(models.Model):
    package = models.ForeignKey(StudentExamPackage, on_delete=models.CASCADE)
    sub = models.ForeignKey(StudentExamSubPackage, on_delete=models.CASCADE)



class StudentMainExam(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    main = models.ForeignKey(MainExam, on_delete=models.SET_NULL, null=True)
    IStudent = models.ForeignKey(Front_student_data, on_delete=models.CASCADE, null=True)
    EStudent = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    instruction = RichTextUploadingField(blank=True, null=True)
    syllabus = models.FileField(null=True, blank=True)
    time_taken = models.CharField(max_length=100, default="00:00")
    time_remain = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="Unseen")
    your_marks = models.CharField(max_length=100, default="0")
    accuracy = models.CharField(max_length=100, default="0")
    attempt = models.CharField(max_length=100, default="0")
    present_question_id = models.CharField(max_length=100, default="0")
    date = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self):
        return self.name


class StudentSubPackage_MainExam(models.Model):
    sub = models.ForeignKey(StudentExamSubPackage, on_delete=models.CASCADE)
    main = models.ForeignKey(StudentMainExam, on_delete=models.CASCADE)



class StudentMainExamSection(models.Model):
    exam = models.ForeignKey(StudentMainExam, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class StudentExamQuestion(models.Model):
    MainSection = models.ForeignKey(StudentMainExamSection, on_delete=models.CASCADE)
    Question = models.ForeignKey(StudentQuestions, on_delete=models.CASCADE)
    time_taken = models.CharField(max_length=100, default="00:00")
    status = models.CharField(max_length=100, default = "Unseen")
    status2 = models.CharField(max_length=100, default = "UnTag")

    Type1Ans = models.CharField(max_length=100, default = "0")
    Type2Ans1 = models.BooleanField(default=False)
    Type2Ans2 = models.BooleanField(default=False)
    Type2Ans3 = models.BooleanField(default=False)
    Type2Ans4 = models.BooleanField(default=False)

    Type3Ans1 = models.CharField(max_length=250, null=True, blank=True)
    Type3Ans2 = models.CharField(max_length=250, null=True, blank=True)


    Type4Ans = models.CharField(max_length=250, null=True, blank=True)


''' ******* End Student Assign Exam Package MoDEL ******'''


''' ******* Start Student Assign Quiz Package MoDEL ******'''

class StudentQuizPackage(models.Model):
    course = models.ForeignKey(Sub_course, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    fee = models.CharField(max_length=10, null=True, blank=True, default=0)
    o_fee = models.CharField(max_length=10, null=True, blank=True, default=0)
    syllabus = models.FileField(null=True, blank=True)

class StudentQuiz(models.Model):
    course = models.ForeignKey(Sub_course, null=True)
    main = models.ForeignKey(Quiz, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    IStudent = models.ForeignKey(Front_student_data, on_delete=models.CASCADE, null=True)
    EStudent = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE, null=True)

    time_taken = models.CharField(max_length=100, default="00:00")
    time_remain = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default="Unseen")
    your_marks = models.CharField(max_length=100, default="0")
    accuracy = models.CharField(max_length=100, default="0")
    attempt = models.CharField(max_length=100, default="0")
    present_question_id = models.CharField(max_length=100, default="0")
    date = models.CharField(max_length=100, null=True, blank=True)


class StudentQuiz_QuizPackage(models.Model):
    package = models.ForeignKey(StudentQuizPackage, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(StudentQuiz, on_delete=models.CASCADE, null=True)


class StudentQuiz_Questions(models.Model):
    quiz = models.ForeignKey(StudentQuiz, on_delete=models.CASCADE)
    Question = models.ForeignKey(StudentQuestions, on_delete=models.CASCADE)
    time_taken = models.CharField(max_length=100, default="00:00")
    status = models.CharField(max_length=100, default="Unseen")
    status2 = models.CharField(max_length=100, default="UnTag")

    Type1Ans = models.CharField(max_length=100, default="0")
    Type2Ans1 = models.BooleanField(default=False)
    Type2Ans2 = models.BooleanField(default=False)
    Type2Ans3 = models.BooleanField(default=False)
    Type2Ans4 = models.BooleanField(default=False)

    Type3Ans1 = models.CharField(max_length=250, null=True, blank=True)

    Type4Ans = models.CharField(max_length=250, null=True, blank=True)

''' ******* End Student Assign Quiz Package MoDEL ******'''



class Assign_Test_Series_Institute_Student(models.Model):
    student = models.ForeignKey(Front_student_data, on_delete=models.CASCADE, null=True)
    real = models.ForeignKey(ExamPackage, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(StudentExamPackage, on_delete=models.CASCADE, null=True)
    total_fee = models.CharField(max_length=150, null=True, blank=True)
    paid_fee = models.CharField(max_length=150, null=True, blank=True)
    remain_fee = models.CharField(max_length=150, null=True, blank=True)
    date = models.CharField(max_length=150, null=True, blank=True)



class Assign_Test_Series_External_Student(models.Model):
    student = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(StudentExamPackage, on_delete=models.CASCADE, null=True)
    real = models.ForeignKey(ExamPackage, on_delete=models.SET_NULL, null=True)
    total_fee = models.CharField(max_length=150, null=True, blank=True)
    paid_fee = models.CharField(max_length=150, null=True, blank=True)
    remain_fee = models.CharField(max_length=150, null=True, blank=True)
    date = models.CharField(max_length=150, null=True, blank=True)



class Assign_Quiz_Institute_Student(models.Model):
    student = models.ForeignKey(Front_student_data, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(StudentQuizPackage, on_delete=models.CASCADE, null=True)
    real = models.ForeignKey(QuizPackage, on_delete=models.SET_NULL, null=True)
    total_fee = models.CharField(max_length=150, null=True, blank=True)
    paid_fee = models.CharField(max_length=150, null=True, blank=True)
    remain_fee = models.CharField(max_length=150, null=True, blank=True)
    date = models.CharField(max_length=150, null=True, blank=True)



class Assign_Quiz_External_Student(models.Model):
    student = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(StudentQuizPackage, on_delete=models.CASCADE, null=True)
    real = models.ForeignKey(QuizPackage, on_delete=models.SET_NULL, null=True)
    total_fee = models.CharField(max_length=150, null=True, blank=True)
    paid_fee = models.CharField(max_length=150, null=True, blank=True)
    remain_fee = models.CharField(max_length=150, null=True, blank=True)
    date = models.CharField(max_length=150, null=True, blank=True)


class Assign_Study_Institute_Student(models.Model):
    student = models.ForeignKey(Front_student_data, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(DailyPracticeSubject, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=150, null=True, blank=True)


class Assign_Study_External_Student(models.Model):
    student = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(DailyPracticeSubject, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=150, null=True, blank=True)


class InvoiceNumber(models.Model):
    start_char = models.CharField(max_length=100, null=True, blank=True)
    num = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.num


class ExamInvoiceGenerate(models.Model):
    invoice = models.CharField(max_length=100, null=True, blank=True)
    exam = models.ForeignKey(Assign_Test_Series_Institute_Student, on_delete=models.CASCADE, null=True)
    quiz = models.ForeignKey(Assign_Quiz_Institute_Student, on_delete=models.CASCADE, null=True)
    o_exam = models.ForeignKey(Assign_Test_Series_External_Student, on_delete=models.CASCADE, null=True)
    o_quiz = models.ForeignKey(Assign_Quiz_External_Student, on_delete=models.CASCADE, null=True)
    total_fee = models.CharField(max_length=100, null=True, blank=True)
    paid_fee = models.CharField(max_length=100, null=True, blank=True)
    remain_fee = models.CharField(max_length=100, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=100, null=True, blank=True)



class StudentGroup(models.Model):
    date = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=300, null=True)


class Group_Students(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(Add_New_Student, on_delete=models.CASCADE)




