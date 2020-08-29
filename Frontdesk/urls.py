from django.conf.urls import url,include
from django.contrib import admin
from Frontdesk.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Frontdesk"
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', home,name = 'home'),
    url(r'^all_students/$', Front_all_student,name = 'front_all_student'),
    url(r'^student/(?P<option>[\w-]+)/(?P<sid>[0-9]+)/$', Front_view_edit_student,name = 'front_VED_student'),
    url(r'^student-addmission/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)/(?P<enquiry_id>[\w-]+)/$', Front_add_student,name = 'front_add_student'),
    url(r'^Asign_course/(?P<stu_id>[0-9]+)/(?P<cor>[0-9]+)/(?P<bat>[0-9]+)/$', Front_AsignCourse_ToStudent, name='front_asign_course'),

    ######Enquiry#######
    url(r'^AllEnquiry/$', Front_enquiry, name='front_enquiry'),
    url(r'^Enquiry/(?P<eid>[0-9]+)/(?P<option>[\w-]+)/$', Front_close_or_update_enquiry, name='front_close_or_update'),

    url(r'^enquiry_followup_Reminder/$', Front_enquiry_followup_reminder, name='front_enquiry_followup_reminder'),
    url(r'^enquiry_Previous_followup/$', Front_previous_follow_up, name='front_enquiry_previous_followup'),
    url(r'^import_enquiry/$', Front_Import_Enquiry, name='front_import_enquiry'),

######### Fee Pay ############
    url(r'^student_Fee_details/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)/$', Front_student_collect_fee, name='front_fee_details'),
    url(r'^Fee_collection_reminder/$', Front_fee_collection_reminder, name='front_fee_collection_reminder'),
    url(r'^Copmplete_Fee_paid_list/$', Front_Complete_FeePaidList, name='front_complete_fee_paid'),

########## All Courses and THeir Details ###########
    url(r'^AllCourse/$', Front_Total_Courses, name='front_total_course'),
    url(r'^Course_Details/(?P<course_id>[0-9]+)$', Front_Course_Details, name='front_details_course'),


########### Cancal Addmission ################</a>
    url(r'^student_cancal_addmission/$', Front_CancalAddmission, name='front_cancal_addmission'),

    url(r'^student_cancal_addmission_List/(?P<cor>[\w-]+)/$', Front_Cancal_AddmissionList, name='front_cancal_addmission_list'),

########## Filter Students ############
    url(r'^filter_students/(?P<cor>[\w-]+)/(?P<bat>[\w-]+)/$', Front_filter_students, name='front_filter_student'),

########### Generate Invoice ###########
    url(r'^student_invoice/(?P<pid>[0-9]+)/$', Front_generate_invoice, name='front_student_invoice'),
################## Upload Document#########

    url(r'^Document/(?P<cor>[0-9]+)/(?P<opt>[\w-]+)/$', Front_UploadDoc_or_GenerateIdCard, name='front_upload_doc_or_idcard'),
    url(r'^student/(?P<sid>[0-9]+)/(?P<op>[\w-]+)/$', Front_single_student_doc_idcard, name='front_single_s_doc_id'),
    url(r'^All_uploaded_Documents/$', All_Batch_uploaded_documents, name='front_all_uploded'),
    url(r'^All_Receipts/$', Front_all_receipts, name='front_all_receipts'),
    url(r'^Staff_id_cards/$', Front_staff_id_card, name='front_staff_idcard'),
   #################### Notification #################
   url(r'^notification_batch/(?P<cour>[\w-]+)/(?P<batch>[\w-]+)/$', Notification_for_Batch, name='notification_batch'),
   url(r'^notification_for_all_students/(?P<option>[\w-]+)/$', Notification_for_allstudents_or_staff, name='notification_all_stu_or_staff'),
   url(r'^select_student/(?P<cour>[\w-]+)/(?P<batch>[\w-]+)/$',
        Select_student_for_notifi, name='select_student'),
   url(r'^Select_Enquiry_student/(?P<cor>[\w-]+)/$', Select_enquiry_students, name='select_enq_students'),
   url(r'^Notification_for_Enquiry_student/(?P<enq_data>[\w-]+)/$', Notification_Enquiry_students, name='notification_enquiry_student'),



   url(r'^notification_for_single_student/(?P<ndata>[\w-]+)/$', Notification_for_single_student, name='notification_for_single'),
   url(r'^notification_for_single_staff/$', Notification_for_single_staff, name='notification_for_single_staff'),
   #############Call Logs #################
   url(r'^all_call_logs/$', Front_student_call_logs, name='call_logs'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


