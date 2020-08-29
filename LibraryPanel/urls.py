from django.conf.urls import url,include
from django.contrib import admin
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "LibraryPanel"
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Library_Deshboard,name = 'library_deshboard'),
    url(r'^Add_category/$', Library_Add_Category,name = 'Library_add_cat'),
    url(r'^Book_List/(?P<opt>[\w-]+)/$', Library_Book_List,name = 'Library_book_List'),
    url(r'^Add_Book_Sub_Category/$', Library_add_sub_category,name = 'Library_add_sub_cat'),
    url(r'^Library_add_books/(?P<cat>[\w-]+)/$', Library_Add_Books,name = 'Library_add_books'),
    url(r'^Library_books_Details/(?P<bid>[0-9]+)/$', Library_book_details,name = 'Library_book_details'),
    url(r'^Library_books_Edit_Details/(?P<bid>[0-9]+)/(?P<cat>[0-9]+)/(?P<subcat>[0-9]+)$', Library_Book_Edit_Details,name = 'Library_book_edit'),
    url(r'^Library_online_books/$', Library_Online_Book, name = 'Library_online_book'),
    url(r'^Library_e_books_Edit_Details/(?P<bid>[0-9]+)/(?P<cat>[0-9]+)/(?P<subcat>[0-9]+)$', Library_E_Book_Edit_Details,
        name='Library_e_book_edit'),

    url(r'^Library_add_e_books/(?P<cat>[\w-]+)/$', Library_E_Add_Books, name='Library_add_e_books'),
    url(r'^Library_delete_e_book/(?P<bid>[0-9]+)/$', Library_Online_Delete_Book, name='Library_delete_book'),

    url(r'^Library_issue_books/(?P<student_data>[\w-]+)/(?P<bid>[0-9]+)/$', Library_Book_Issue, name = 'Library_issue_book'),
    url(r'^Filter_rollNumber/$', Filter_RollNumber, name='filter_roll_number'),

    url(r'^Library_issued_books/$', Library_Issued_Books, name = 'Library_issued_book'),
    url(r'^Library_Return_Book/(?P<bid>[0-9]+)/$', Library_Return_Book,name = 'Library_Return_Book'),
    url(r'^Library_Return_Book_list/$', Issue_Book_Return,name = 'Library_Return_Book_list'),
    url(r'^Stuednt_library_fine_list/$', Library_Student_Fine_List,name = 'Library_fine_list'),
    url(r'^Delete/(?P<num>[0-9]+)/(?P<type>[\w-]+)/$', Delete_for_all,
        name='delete_for_all'),
    url(r'^UnCategorized_books/$', Uncategorized_books, name='un_cat_book'),
    url(r'^Asign_catagory/(?P<cate>[0-9]+)/(?P<bid>[0-9]+)/$', Asign_category_to_book, name='asign_cat'),


]