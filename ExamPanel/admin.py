from django.contrib import admin

from .models import *

admin.site.register(ExamPackage)
admin.site.register(MainExam)
admin.site.register(MultipleChoiceQuestions)
admin.site.register(SubPackage_MainExam)
admin.site.register(ExamSubPackage)
admin.site.register(Package_Subpackage)
admin.site.register(Assign_Test_Series_Institute_Student)

admin.site.register(StudentExamPackage)
admin.site.register(StudentExamSubPackage)
admin.site.register(StudentPackage_Subpackage)
admin.site.register(StudentMainExam)
admin.site.register(StudentSubPackage_MainExam)
admin.site.register(StudentMainExamSection)
admin.site.register(StudentExamQuestion)



admin.site.register(QuizPackage)
admin.site.register(Quiz_QuizPackage)
admin.site.register(Quiz_Questions)
admin.site.register(Quiz)


admin.site.register(StudentQuizPackage)
admin.site.register(StudentQuiz_QuizPackage)
admin.site.register(StudentQuiz_Questions)
admin.site.register(StudentQuiz)
admin.site.register(StudentQuestions)


admin.site.register(Group_Students)



admin.site.register(Add_New_Student)
admin.site.register(InvoiceNumber)
admin.site.register(ExamInvoiceGenerate)