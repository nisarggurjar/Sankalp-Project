from django.conf.urls import url,include
from django.contrib import admin
from Institute.views import *
from django.conf import settings
from django.conf.urls.static import static
from WebSite.views import *


urlpatterns = [
    url(r'^register/$', Register, name = "register"),
    url(r'^forgot_password/$', ForgotPass, name = "Forgot"),
    url(r'^login/$', Login, name = "login"),
    url(r'^$', Website_home, name = "website_home"),
    url(r'^SkyLark/$', Start, name = "demo"),
    url(r'^logout$', Logout, name = "logout"),
    url(r'^frontdesk/', include('Frontdesk.urls', namespace='Frontdesk')),
    url(r'^Student_panel/', include('Student.urls', namespace='StudentPanel')),
    url(r'^website/', include('WebSite.urls', namespace='Website')),

    url(r'^exam_controller/', include('ExamPanel.urls', namespace='ExamPanel')),
    url(r'^library_panel/', include('LibraryPanel.urls', namespace='LibraryPanel')),
    url(r'^master_panel/', include('Institute.urls', namespace='Master')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





