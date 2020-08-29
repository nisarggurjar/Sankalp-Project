from django.conf.urls import url,include
from django.contrib import admin
from Institute.views import *
from django.conf import settings
from django.conf.urls.static import static
from home.views import *


urlpatterns = [
    url(r'^register/$', Register, name = "register"),
    url(r'^forgot_password/$', ForgotPass, name = "Forgot"),
    url(r'^login/$', Login, name = "login"),
    url(r'^SkyLark/$', Start, name = "demo"),
    url(r'^logout$', Logout, name = "logout"),
    url(r'^frontdesk/', include('Frontdesk.urls', namespace='Frontdesk')),
    url(r'^Student_panel/', include('Student.urls', namespace='StudentPanel')),

    url(r'^exam_controller/', include('ExamPanel.urls', namespace='ExamPanel')),
    url(r'^library_panel/', include('LibraryPanel.urls', namespace='LibraryPanel')),
    url(r'^master_panel/', include('Institute.urls', namespace='Master')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),


    url(r'^$', home, name = "home"),
    url(r'^training/$', training, name = "training"),
    url(r'^get-in-touch/$', contact, name="contact"),
    url(r'^about-us/$', about, name="about"),
    url(r'^send_mail$', Send_Mail, name="send_mail"),
    url(r'^new_batch_registration', New, name="batch"),
url(r'^sitemap', Sitemap, name="sitemap"),
    url(r'^Master-Course/(?P<value>[\w-]+)/$', python, name="master"),
	url(r'^training/(?P<value>[\w-]+)/$', web, name="web"),
    url(r'^change_sub_headings/(?P<num>[0-9]+)/$', Change_Sub_Heading, name='edit_sub_headings'),
    url(r'^change_headings/(?P<num>[0-9]+)/$', Change_Heading, name='edit_headings'),
url(r'^delete_headings/(?P<num>[0-9]+)/$', Delete_Heading, name='delete_headings'),

    url(r'^certificate/$', Search_Certi, name="certificate"),
    url(r'^certificate/(?P<num>[\w-]+)/$', Certi_View, name="certificate_online"),
    url(r'^add_college/$', Add_College, name="add_college"),
    url(r'^add_course/$', Add_Course, name="add_course"),
    url(r'^add_certificate/$', Add_Certificate, name="add_certificate"),
    url(r'^certificate_master/$', Certificate_Master, name="certificate_master"),
  url(r'^page_not_found/$', error_404, name="error"),

]

handler404 = error_404
handler500 = error_500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





