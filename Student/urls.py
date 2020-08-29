from django.conf.urls import url,include
from django.contrib import admin
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "StudentPanel"
urlpatterns = [
url(r'^admin/', admin.site.urls),
url(r'^$', Dashboard, name = 'home'),
url(r'^Add_link/(?P<option>[\w-]+)/$', Students_Link_add, name = 'students_links'),
url(r'^profile/$', Student_profile, name = 'profile'),
url(r'^Change_password/$', Chenge_password, name = 'change_password'),
url(r'^Edit_profile/$', Student_edit_profile, name = 'edit_profile'),
url(r'^test_list/$', AllTests, name = 'tests'),
url(r'^exams_list/(?P<pid>[\w-]+)/$', All_Exams, name = 'exams'),
url(r'^Generate_invoice/(?P<pid>[0-9]+)/$', Student_generate_invoice, name = 'invoice'),




url(r'^test_instruction/(?P<eid>[\w-]+)/$', TestInstruction, name = 'instruction'),
url(r'^test_live/exam/(?P<eid>[\w-]+)/section/(?P<sid>[\w-]+)/question/(?P<qid>[\w-]+)/(?P<num>[\w-]+)/(?P<what>[\w-]+)/(?P<time>[\w-]+)/$', LiveTest, name = 'live'),
url(r'^analysis/(?P<eid>[\w-]+)/$', TestAnalysis, name = 'analysis'),
url(r'^Exam_Solution/exam/(?P<eid>[\w-]+)/section/(?P<sid>[\w-]+)/question/(?P<qid>[\w-]+)/(?P<num>[\w-]+)/(?P<what>[\w-]+)/(?P<time>[\w-]+)/$', ExamSolution, name = 'solution'),



url(r'^practice/$', Practice, name = 'practice'),
url(r'^practice_questions/$', PracticeQuestion, name = 'practice_questions'),
url(r'^single_question/$', StartPractice, name = 'single_question'),

url(r'^quiz/$', AllQuiz, name = 'quiz'),
url(r'^start_quiz/(?P<qid>[\w-]+)/(?P<q_id>[\w-]+)/(?P<time>[\w-]+)/$', StartQuiz, name = 'start_quiz'),
url(r'^quiz_summery/(?P<qid>[\w-]+)/analysis_Answers/$', QuizSummery, name = 'quiz_summery'),
url(r'^quiz_solution/(?P<qid>[\w-]+)/Answers/(?P<q_id>[\w-]+)/$', QuizSolution, name = 'quiz_solution'),



url(r'^study_material/$', Study_Material, name = 'study_material'),
url(r'^courses/$', Courses, name = 'courses'),
url(r'^fee/$', FeeDetails, name = 'FeeDetails'),
url(r'^invoice/$', Invoice, name = 'invoice'),

url(r'^Installment_details/(?P<cid>[0-9]+)/$', FeeInstallmentDetails, name = 'installment_details'),
url(r'^Notifications/$', Student_Notifications, name = 'student_notification'),
url(r'^Uploaded_Document/$', Student_Upload_Documents, name = 'student_upload_document'),
url(r'^E_corner/$', Student_Ecorner, name = 'student_ecorner'),
url(r'^Issued_Returned_Book/$', Student_issued_returned_book, name = 'issue_return_book'),


]