from django.conf.urls import url,include
from django.contrib import admin
from WebSite.views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "Website"
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', Website_home,name='website_home'),
    url(r'^About_us/$', AboutUs, name='aboutus'),
url(r'^Contact_us/$', ContactUs, name='contact'),
url(r'^Branches/$', Branches, name='branches'),
url(r'^Student_Zone/$', Student_Zone, name='student_zone'),
url(r'^Student_Reviews/$', Student_Reviews, name='student_review'),
url(r'^Student_Query/$', Student_quiry_form, name='student_query'),
url(r'^login/$', Website_admin_login,name='web_login'),
url(r'^logout/$', Website_admin_logout,name='web_logout'),
url(r'^add_slider/$', Website_slider_add,name='web_slider'),
url(r'^delete_slider/(?P<sid>[0-9]+)/$', Website_slider_delete,name='delete_slider'),
url(r'^Add_sub_course/(?P<mid>[0-9]+)/$', Website_add_subcourse,name='web_add_subcourse'),
url(r'^Course_details/(?P<mid>[0-9]+)/$', Main_course_details,name='main_cdetails'),
url(r'^subCourse_details/(?P<sid>[0-9]+)/$', Sub_course_details,name='sub_cdetails'),
url(r'^Chenge_profile/(?P<type>[\w-]+)/$', Change_profile,name='change_profile'),
url(r'^Chenge_Content/(?P<type>[\w-]+)/$', Edit_Welcome_content,name='edit_content'),
url(r'^Chenge_about_content/(?P<type>[\w-]+)/$', Edit_About_Content,name='edit_about_content'),
url(r'^change_image/(?P<option>[\w-]+)/$', Change_image,name='change_image'),
url(r'^Delete_course/(?P<type>[\w-]+)/(?P<num>[0-9]+)$', Delete_stuff,name='delete_stuff'),
url(r'^Edit_course/(?P<num>[0-9]+)$', Edit_Main_course,name='edit_maincourse'),
url(r'^add_course/$', Website_add_course,name='web_add_course'),
url(r'^add_review/$', Add_Review,name='add_review'),
url(r'^add_faculty_review/$', Add_Faculty_Review,name='add_f_review'),
url(r'^add_brand/$', Add_brand,name='add_brand'),
url(r'^Our_Gallery/$', Our_gallery,name='our_gallery'),
url(r'Add_Gallery/$', Add_Gallery,name='add_gallery'),
url(r'^Edit_counter_value/$', Edit_counter,name='edit_counter'),
url(r'^Edit_Subcourse/(?P<type>[\w-]+)/(?P<num>[0-9]+)$', Edit_sub_course,name='edit_subcourse'),
url(r'^Edit_Content/(?P<num>[0-9]+)/$', Edit_course_content,name='edit_course_content'),
url(r'^Add_content/(?P<num>[0-9]+)/$', Add_content,name='add_content'),
url(r'^Add_Sub_course/(?P<num>[0-9]+)/$', Add_sub_course,name='add_sub_course'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)