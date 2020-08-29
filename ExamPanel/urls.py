from django.conf.urls import url,include
from django.contrib import admin
from Institute.views import *
from django.conf import settings
from django.conf.urls.static import static
from ExamPanel.views import *

app_name = "ExamPanel"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/$', Home, name='exam_home'),

    url(r'^create_exam_package/$', CreateExamPackage, name='create_exam_package'),
    url(r'^delete_exam_package/(?P<eid>[0-9]+)/$', DeleteExamPackage, name='delete_package'),
    url(r'^edit_exam_package/(?P<eid>[0-9]+)/$', EditExamPackage, name='edit_package'),
    url(r'^add_exam_sub_packages/(?P<eid>[0-9]+)/$', AddExamSubPackage, name='add_packages'),
    url(r'^remove_sub_packages/(?P<eid>[0-9]+)/$', RemoveSubPackage, name='remove_sub_packages'),
    url(r'^publish_unpublish/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/(?P<what1>[\w-]+)/$', Publish_UnPublish, name='publish'),

    url(r'^create_exam_subpackage/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<what>[\w-]+)$', CreateExamSubPackage,
        name='create_exam_subpackage'),
    url(r'^details_exam_subpackage/(?P<eid>[\w-]+)/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/$', ExamSubPackageDetails,
        name='subpackage_details'),
    url(r'^edit_subpackage/(?P<eid>[0-9]+)/$', EditExamSubPackage, name='edit_subpackage'),
    url(r'^delete_exam_subpackage/(?P<eid>[0-9]+)/$', DeleteExamSubPackage, name='delete_subpackage'),
    url(r'^subpackage_exam_list/(?P<sid>[0-9]+)/$', Sub_Package_Exam_List, name='subpackage_exam_list'),

    url(r'^create_main_exam/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<what>[\w-]+)$', CreateMainExam,
        name='create_main_exam'),
    url(r'^edit_main_exam/(?P<eid>[0-9]+)/$', EditMainExam, name='edit_main'),
    url(r'^delete_main_exam/(?P<eid>[0-9]+)/$', DeleteMainExam, name='delete_main'),
    url(r'^exam_instruction/(?P<eid>[0-9]+)/$', ExamInstructionView, name='exam_instruction'),
    url(r'^main_exam_details/(?P<eid>[0-9]+)/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/$', MainExamDetails,
        name='main_exam_details'),
    url(r'^remove_main_exams/(?P<eid>[0-9]+)/$', RemoveMainExam, name='remove_main_exam'),
    url(r'^edit_student_main_exam/(?P<eid>[0-9]+)/(?P<sid>[\w-]+)/(?P<what>[\w-]+)/(?P<option>[\w-]+)$',
        EditStudentMainExam, name='edit_student_main'),
    url(r'^student_main_exam_sections/(?P<eid>[0-9]+)/$', StudentExamSections, name='student_main_exam_sections'),

    url(r'^create_question_section/(?P<cid>[0-9]+)/(?P<sid>[0-9]+)/(?P<option>[\w-]+)/$', CreateQuestionSection,
        name='create_question_section'),

    url(r'^add_import_questions/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<exam>[\w-]+)/$',
        AddImportQuestions, name='add_import_questions'),
    url(r'^add_main_exam_section/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<exam>[\w-]+)/$',
        AddMainExamSection, name='add_main_exam_section'),
    url(r'^exam_section/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<eid>[0-9]+)/$', ExamSectionCreation,
        name='exam_section'),

    url(r'^delete_exam_section/(?P<sid>[\w-]+)/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<eid>[0-9]+)/$',
        ExamSectionDelete, name='delete_exam_section'),

    # url(r'^all_questions/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<subpack>[\w-]+)/(?P<exam>[\w-]+)/$', AllQuestions, name='all_questions'),
    # url(r'^filter_questions/(?P<cid>[0-9]+)/(?P<pid>[0-9]+)/(?P<spid>[0-9]+)/(?P<eid>[0-9]+)/$', FilteredQuestions, name='filter_questions'),

    url(r'^select_question_type/(?P<sid>[\w-]+)/$', TypeofQuestion, name='select_question_type'),
    url(r'^all_questions/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$', All_Questions,
        name='all_section_questions'),
    url(r'^add_questions_in_exam_section/(?P<s_id>[\w-]+)/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$',
        AddQuestion_In_ExamSection, name='add_questions_in_exam_section'),
    url(r'^add_questions_in_student_exam_section/(?P<s_id>[\w-]+)/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$',
        AddQuestion_In_StudentExamSection, name='add_questions_in_student_exam_section'),
    url(r'^question_bank/(?P<cid>[\w-]+)/(?P<pno>[\w-]+)/$', MyQuestionBank, name='questions_bank'),
    url(r'^import_questions/$', Import_Question, name='import'),
    url(r'^export_sheet/$', export_users_xls, name='export'),
    url(r'^null_questions/(?P<pno>[\w-]+)/(?P<sid>[\w-]+)/$', NullQuestion, name='null_questions'),
    url(r'^exam_sections_questions/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/(?P<what>[\w-]+)/$', ExamSectionQuestionList,
        name='exam_sections_questions'),
    url(r'^student_exam_sections_questions/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/(?P<what>[\w-]+)/$',
        StudentExamSectionQuestionList, name='student_exam_sections_questions'),

    url(r'^add_multi_questions/(?P<eid>[0-9]+)/$', AddMultiQuestions, name='add_multi_questions'),
    url(r'^add_multi_response_questions/(?P<eid>[0-9]+)/$', AddMultiResponseQuestions,
        name='add_multi_response_questions'),
    url(r'^add_fill_questions/(?P<eid>[0-9]+)/$', AddFillInTheBlanksQuestions, name='add_fill_questions'),
    url(r'^add_true_false_questions/(?P<eid>[0-9]+)/$', AddTrueFalseQuestions, name='add_true_false_questions'),

    url(r'^edit_multi_questions/(?P<eid>[0-9]+)/(?P<c_url>[\w-]+)/(?P<what>[\w-]+)/$', EditMultiQuestions,
        name='edit_multi_questions'),
    url(r'^edit_multi_response_questions/(?P<eid>[0-9]+)/(?P<c_url>[\w-]+)/(?P<what>[\w-]+)/$',
        EditMultiResponseQuestions, name='edit_multi_response_questions'),
    url(r'^edit_fill_questions/(?P<eid>[0-9]+)/(?P<c_url>[\w-]+)/(?P<what>[\w-]+)/$', EditFillInTheBlanksQuestions,
        name='edit_fill_questions'),
    url(r'^edit_true_false_questions/(?P<eid>[0-9]+)/(?P<c_url>[\w-]+)/(?P<what>[\w-]+)/$', EditTrueFalseQuestions,
        name='edit_true_false_questions'),

    url(r'^remove_questions/(?P<qid>[0-9]+)/(?P<where>[\w-]+)$', RemoveQuestions, name='remove_questions'),

    # '''Quiz Package Urls'''
    url(r'^create_quiz_package/$', CreateQuizPackage, name='create_quiz_package'),
    url(r'^modify_quiz_package/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/$', EditQuizPackage, name='edit_quiz_package'),
    url(r'^create_quiz/(?P<cour>[\w-]+)/(?P<pack>[\w-]+)/(?P<what>[\w-]+)/$', CreateQuiz, name='create_quiz'),
    url(r'^modify_quiz/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/$', EditQuiz, name='edit_quiz'),
    url(r'^modify_student_quiz/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/(?P<sid>[0-9]+)/(?P<option>[\w-]+)/$', EditStudentQuiz,
        name='edit_student_quiz'),
    url(r'^add_quiz/(?P<eid>[0-9]+)/$', QuizList, name='add_quiz'),
    url(r'^add_questions_in_quiz/(?P<q_id>[\w-]+)/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$',
        AddQuestion_In_Quiz, name='add_questions_in_quiz'),
    url(r'^add_questions_in_student_quiz/(?P<q_id>[\w-]+)/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$',
        AddQuestion_In_Student_Quiz, name='add_questions_in_student_quiz'),
    url(r'^quiz_question_list/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$', QuizQuestionList, name='quiz_question_list'),
    url(r'^student_quiz_question_list/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$', StudentQuizQuestionList,
        name='student_quiz_question_list'),

    # '''Upload Material'''
    url(r'^upload_material/(?P<cour>[\w-]+)/$', UploadMaterial, name='upload_material'),
    url(r'^delete_material/(?P<mid>[\w-]+)/$', DeleteUploadMaterila, name='delete_material'),

    # '''Daily Practice Material'''
    url(r'^daily_practice_material/$', DailyPractice, name='daily_practice_material'),
    url(r'^modify_daily_practice_subject/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/$', EditDailyMaterial,
        name='edit_daily_material'),
    url(r'^daily_practice_topic/(?P<For>[\w-]+)/$', PracticeTopic, name='daily_practice_topic'),
    url(r'^modify_daily_practice_topic/(?P<eid>[0-9]+)/(?P<what>[\w-]+)/$', EditPracticeTopic,
        name='edit_practice_topic'),
    url(r'^add_questions_in_topic/(?P<q_id>[\w-]+)/(?P<cid>[\w-]+)/(?P<sid>[\w-]+)/(?P<pno>[\w-]+)/$',
        AddQuestion_In_Topic, name='add_questions_in_topic'),
    url(r'^practice_topic_question/(?P<sid>[0-9]+)/(?P<pno>[\w-]+)/$', TopicQuestionList,
        name='practice_topic_question'),

    # '''''''' Students And Assign Packages'''''
    url(r'^institute_students_list/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)$', Institute_students,
        name='institute_students_list'),
    url(r'^institute_students_view/(?P<option>[\w-]+)/(?P<sid>[\w-]+)/$', Institute_view_student,
        name='institute_students_view'),
    url(r'^assign_test_package/(?P<stu_id>[\w-]+)/(?P<cour>[\w-]+)/(?P<test>[\w-]+)/(?P<decide>[\w-]+)$',
        Assign_test_package_Students, name='assign_test_package'),
    url(r'^assign_quiz_package/(?P<stu_id>[\w-]+)/(?P<cour>[\w-]+)/(?P<quiz>[\w-]+)/(?P<decide>[\w-]+)$',
        Assign_quiz_package_Students, name='assign__quiz'),
    url(r'^assign_study_package/(?P<stu_id>[\w-]+)/(?P<cour>[\w-]+)/(?P<study>[\w-]+)/(?P<decide>[\w-]+)$',
        Assign_Study_Material_Students, name='assign__study'),
    url(r'^cancel_packages/(?P<what>[\w-]+)/(?P<decide>[\w-]+)/$', Cancel_all, name='cancel_packages'),

    url(r'^add_new_students/$', AddNewStudents, name='add_new_students'),
    url(r'^update_new_students/(?P<sid>[\w-]+)/(?P<what>[\w-]+)/$', Edit_Delete_Other_Students,
        name='edit_new_students'),
    url(r'^other_students_view/(?P<option>[\w-]+)/(?P<sid>[\w-]+)/$', Other_view_student, name='other_students_view'),
    url(r'^pay_fee/(?P<pid>[\w-]+)/(?P<what>[\w-]+)/(?P<option>[\w-]+)/$', Pay_Test_Quiz_Fee, name='pay_test_quiz_fee'),

    url(r'^new_students_group/$', Student_Groups, name='new_students_group'),
    url(r'^delete_students_group/(?P<gid>[\w-]+)/$', Student_Groups_Delete, name='delete_students_group'),
    url(r'^add_students_in_group/(?P<gid>[\w-]+)/$', Add_Students_In_Group, name='add_students_in_group'),
    url(r'^students_in_group_list/(?P<gid>[\w-]+)/$', Group_Student_List, name='group_students_list'),

    url(r'^assign_test_package_to_groups/(?P<cid>[\w-]+)/(?P<bid>[\w-]+)/(?P<eid>[\w-]+)/(?P<option>[\w-]+)$',
        Assign_Test_Series_to_Groups, name='assign_test_package_to_groups'),
    url(r'^assign_quiz_package_to_groups/(?P<cid>[\w-]+)/(?P<bid>[\w-]+)/(?P<eid>[\w-]+)/(?P<option>[\w-]+)$',
        Assign_Quizes_to_Groups, name='assign_quiz_package_to_groups'),
    url(r'^assign_study_package_to_groups/(?P<cid>[\w-]+)/(?P<bid>[\w-]+)/(?P<eid>[\w-]+)/(?P<option>[\w-]+)$',
        Assign_Study_Material_Groups, name='assign_study_package_to_groups'),
    url(r'^assign_student_list/(?P<eid>[\w-]+)/(?P<what>[\w-]+)/(?P<option>[\w-]+)$', Assigned_Students,
        name='assign_student_list'),

    url(r'^Genearte_exam-invoice/(?P<pid>[0-9]+)/$', Exam_generate_invoice, name='exam_generate_invoice'),

url(r'^package_result/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)/(?P<eid>[\w-]+)$', Test_Package_Result, name='package_result'),
url(r'^quiz_result/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)/(?P<eid>[\w-]+)$', Quiz_Package_Result, name='quiz_result'),

    ]




