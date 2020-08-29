from django.conf.urls import url,include
from django.contrib import admin
from Institute.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Master"
urlpatterns = [
############ Add Delete Edit ##################
    url(r'add/(?P<type>[\w-]+)', Add_to_data, name="add"),
    url(r'delete/(?P<num>[0-9]+)/(?P<type>[\w-]+)/$', Delete_All, name = "delete"),
    url(r'Edit_details/(?P<num>[0-9]+)/(?P<type>[\w-]+)/$', Master_Edit_for_all, name = "edit"),
    url(r'Edit_last_date/(?P<num>[0-9]+)/$', Edit_installment_last_date, name = "edit_last_date"),
    url(r'Edit_installment/(?P<num>[0-9]+)/$', Edit_installment, name="edit_ins"),

    ###############################################
    url(r'^admin/', admin.site.urls),
    url(r'^master_deshboard/$', Master_Deshboard,name='master_deshboard'),
    url(r'^$', Admin_Choose_Institute,name='choose_institute'),
    url(r'^courses/$', Master_course_module,name='master_course'),
    url(r'^fee_type/$',Master_fee_type ,name='master_fee' ),
    url(r'^master_fee_packege/$', Master_fee_packege, name='master_packege'),
    url(r'^master_fee_packege/add/$', Master_add_fee_packege, name='master_add_packege'),
    url(r'^master_fee_packege/Choose_packege/$', Number_of_installment, name='number_of_installment'),
    url(r'^make_installment/(?P<course_packege>[\w-]+)/(?P<number>[\w-]+)/$', Master_make_installment,
        name='master_installment'),
    url(r'^master_fee_packege/details/(?P<fid>[0-9]+)/$',Master_fee_packege_details ,name='master_details_packege' ),
    url(r'^master_medium/$',Master_medium ,name='master_medium' ),
    url(r'^master_batch/$', Master_batch, name='master_batch'),
    url(r'^Fee_last_date/(?P<cid>[0-9]+)/$',Master_last_date_ins ,name='last_date' ),
    url(r'^master_designation/$',Master_designation ,name='master_desig' ),

#### for master sms sender id ########

    url(r'^master_sender_id/$',Master_sms_id ,name='master_sid' ),

#### for master SMA Template ########

    url(r'^master_sms_template/$', SMS_Templates_List, name='master_stemp'),
    url(r'^master_create_sms_template/$', Create_SMS_Template, name='master_create_stemp'),
    url(r'^Book_Fine/$', Master_create_library_fine, name='master_book_fine'),

    #### for master subject########

    url(r'^master_subject/$', Master_subject, name='master_subject'),
   #### for master inventory ########

    url(r'^master_inventory/$', Master_inventory, name='master_inventory'),

    #### for master vendor ########

    url(r'^master_vendor/$', Master_vendor, name='master_vendor'),

    #### for master terms and condition ########

    url(r'^master_terms_condition/$', Master_terms_con, name='master_terms'),

    #### for master Holiday########

    url(r'^master_holiday/$', Master_holiday, name='master_holiday'),

    #### for master email template ########

    url(r'^master_email_template/$', Master_email_temp, name='master_etemp'),
url(r'^change_invoice_number/(?P<option>[\w-]+)/$', Admin_Start_Invoice_number, name='invoice_number'),
url(r'^sms_pack_report/$', SmsPackReport, name='sms_report'),
url(r'^student_pack_report/$', Students_Pack_Report, name='student_report'),
url(r'^sms_fail/$', SMS_Fail, name='sms_fail'),
url(r'^student_fail/$', Student_Fail, name='student_fail'),

######################Students Urls###################
url(r'^All_students/$', Admin_all_students, name='admin_all_student'),
url(r'^Todays_addmission_list/$', Admin_todays_addmission, name='admin_tday_addm_list'),
url(r'^All_fee_receipts/$', Admin_All_Fee_Receipt, name='admin_all_receipts'),
url(r'^All_Student_fee_report/(?P<cor>[0-9]+)/(?P<bat>[0-9]+)$', Admin_Student_fee_report, name='admin_fee_report'),
url(r'^All_open_enquiry/$', Admin_open_enquiry, name='admin_all_open_enq'),
url(r'^All_close_enquiry/$', Admin_close_enquiry, name='admin_all_close_enq'),
url(r'^All_todays_enquiry/$', Admin_todays_enquiry, name='admin_all_todays_enq'),
url(r'^All_todays_followup/$', Admin_todays_follow_ups, name='admin_todays_followup'),
url(r'^Upcoming_follow_ups/$', Admin_upcoming_follow_ups, name='admin_upcoming_followup'),
url(r'^All_cancal_addmission_list/$', Admin_All_cancal_addmission, name='admin_all_cancal_add'),
url(r'^All_External_enquiry/$', Admin_All_External_follow_up, name='admin_all_external_enq'),
url(r'^student_due_fee_report/$', Admin_fee_reminders, name='admin_fee_reminder'),

###################### Library Urls #######################
url(r'^All_Category/$', Admin_All_category, name='admin_all_cat'),
url(r'^All_books/$', Admin_All_Books, name='admin_all_book'),
url(r'^All_E_books/$', Admin_All_E_books, name='admin_all_e_book'),
url(r'^All_issued_book/$', Admin_All_Issued_Books, name='admin_all_issued_book'),
url(r'^All_return_book/$', Admin_All_Issued_return_book, name='admin_all_return_book'),
url(r'^All_subcategory/$', Admin_All_subcategory, name='admin_all_subcat'),
url(r'^All_uncat_book/$', Admin_All_uncat_book, name='admin_all_uncat'),


##################### Frontdesk Function ####################
url(r'^All_previous_follow_up/$', Admin_previous_follow_ups, name='admin_prev_followup'),
url(r'^All_Uploaded_files/$', Admin_All_Batch_uploaded_documents, name='admin_all_upload_files'),
url(r'^upload_new_file/(?P<cor>[0-9]+)/$', Admin_upload_new_files, name='admin_upload_new_file'),
url(r'^Notification_for_batch/(?P<cour>[0-9]+)/(?P<batch>[0-9]+)$', Admin_notification_for_batch, name='admin_noti_for_batch'),
url(r'^Send_notification/(?P<cour>[0-9]+)/(?P<batch>[0-9]+)$', Admin_Select_student_for_notifi, name='admin_select_student'),
url(r'^Notification_for_student/(?P<ndata>[\w-]+)/$', Admin_notification_for_individual, name='admin_notification_for_single'),
url(r'^Notification_for_staff/$', Admin_notification_for_all_staff, name='admin_noti_for_all_staff'),
url(r'^Notification_for_single_staff/$', Admin_notification_for_single_staff, name='admin_noti_for_single_staff'),
url(r'^Select_enquiry_students/(?P<cor>[0-9]+)/$', Admin_Select_enquiry_students, name='admin_select_enquiry_student'),
url(r'^Send_notification_to_enquiry_students/(?P<enq_data>[0-9]+)/$', Admin_Notification_Enquiry_students, name='admin_notification_enq'),


########################## Employee Functions ####################
url(r'^Add_employee/$', Admin_add_employe, name='admin_add_employe'),
url(r'^master_employee/$', Master_employee, name='master_employee'),
url(r'^master_employee_details/(?P<num>[0-9]+)/(?P<type>[\w-]+)/$', Admin_VED_employee, name='admin_VED_employee'),

################### Sales Urls ####################
url(r'^Course_wise_sales/$', Admin_Course_wise_sales, name='admin_wise_sales'),
url(r'^Exam_Packege_wise_sales/$', Admin_Total_packeges_sales, name='admin_pac_wise_sales'),
url(r'^Quiz_Packege_wise_sales/$', Admin_Quiz_sales_report, name='admin_quizpac_wise_sales'),



############################## Reports urls ###################
url(r'^Fee_installment_due_fee_report/$', Admin_Due_fee_report, name='admin_due_fee_report'),
url(r'^Upcoming_fee_installment_report/$', Admin_upcoming_fee_report, name='admin_up_fee_report'),
url(r'^receivable_amount_list/$', Admin_receivable_amount, name='admin_receivable_amount'),
url(r'^Addmission_report/$', Admin_addmission_report, name='admin_addmission_report'),
url(r'^Enquiry_report/$', Admin_Enquiry_report, name='admin_enquiry_report'),
url(r'^Follow_up_report/$', Admin_followup_report, name='admin_follow_up_report'),
url(r'^call_log_report/$', Admin_call_log_report, name='admin_call_log_report'),
url(r'^select_month_year/$', Admin_Select_Month_year, name='admin_select_month_year'),

url(r'^admin_monthly_collection/(?P<mo>[0-9]+)/(?P<ye>[0-9]+)$', Admin_Monthly_Fee_collection_Report, name='admin_monthly_collection'),
########################### Settings Urls #############################
url(r'^Institut_Profile/$', Admin_Institute_profile, name='admin_institute_profile'),
url(r'^New_Institute_Profile/$', Admin_New_Institute_profile, name='admin_add_institute_profile'),
url(r'^Edit_Institut_Profile/$', Edit_institute_profile, name='edit_institute_profile'),
url(r'^Auto_SMS_Setting/$', Admin_Auto_SMS_Setting, name='auto_sms_settings'),
url(r'^user_management_Setting/$', Admin_User_Management, name='user_management_settings'),

url(r'^admin_Profile/$', Adminprofile, name='admin_profile'),
url(r'^Edit_admin_Profile/$', Edit_Admin_profile, name='edit_admin_profile'),







]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
