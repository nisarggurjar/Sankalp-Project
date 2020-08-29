from django.shortcuts import render, redirect
from.models import *
from .forms import *
from datetime import date,datetime
from Frontdesk.views import *
from django.http import HttpResponse


def is_admin(user):
    if user.last_name == "Admin":
        return True
    return False

def is_Librarian(user):
    if user.last_name == "Library":
        return True
    return False

def Issued_Percentage(ins):
    all_books = Master_book_data.objects.filter(ins = ins).order_by('-id')
    t = 0
    for i in all_books:
        t += int(i.copies)
    all_issued_book = Library_Issue_Book.objects.filter(status='Issued').order_by('-id')
    per = 0
    if t>0:
        per = (len(all_issued_book)*100)/t
        per = float("{0:.2f}".format(per))
    return int(per)


def Library_Deshboard(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    total_book = 0
    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
    all_issued_book = Library_Issue_Book.objects.filter(ins = ins,status = 'Issued').order_by('-id')
    last_five = all_issued_book[0:5]
    all_books = Master_book_data.objects.filter(ins = ins).order_by('-id')
    total_ebook = Master_E_Book.objects.filter(ins = ins).count()
    all_un_cat_book = Master_book_data.objects.filter(ins = ins,category = None,subcategory = None)
    todys_issued_book = Library_Issue_Book.objects.filter(ins = ins,issue = format_date,status = 'Issued')
    todays_return_book = Library_Issue_Book.objects.filter(ins = ins,Return = format_date,status ='Returned')
    for book in all_books:
        total_book = total_book + int(book.copies)
    last_five_add = all_books[0:6]
    context = {"last_five":last_five,"last_five_add":last_five_add,"all_issued_book":all_issued_book,
               "total_book":total_book,"total_ebook":total_ebook,"all_un_cat_book":len(all_un_cat_book),
               "todys_issued_book":len(todys_issued_book),"todays_return_book":len(todays_return_book)
               ,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)}

    return render(request,'Library/library_deshboard.html',context)


def Library_Add_Category(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_cat = Master_catbook_data.objects.filter(ins = ins)
    if request.method == "POST":
        cat_book = request.POST['cat_book']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_catbook_data.objects.create(ins = ins, name=cat_book, created_date=format_date)
        return redirect("LibraryPanel:Library_add_cat")
    return render(request,'Library/master_cat_book.html',{"all_cat":all_cat,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)})


def Library_add_sub_category(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_cat = Master_catbook_data.objects.filter(ins = ins)
    if request.method == "POST":
        cat_book = request.POST['cat_book']
        cat = Master_catbook_data.objects.filter(id = cat_book).first()
        subcat_book = request.POST['subcat_book']
        today = date.today()
        format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
        Master_subcatbook_data.objects.create(ins = ins, category=cat, name=subcat_book, created_date=format_date)
        return redirect('LibraryPanel:Library_add_sub_cat')
    return render(request,'Library/master_sub_book.html',{"all_cat":all_cat,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)})

def Library_Book_List(request,opt):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_book =  Master_book_data.objects.filter(ins = ins)
    li = []
    for bk in all_book:
        book = Master_book_data.objects.filter(id = bk.id).first()
        data = Library_Issue_Book.objects.filter(book =book,status = 'Issued')
        if data:
            li.append(bk)

    return render(request,'Library/master_book.html',{"all_book":all_book,"opt":opt,"li":li,"adminprofile":Admin_data(),
                                                      "ins_data":Institute_data(request.user), 'isu':Issued_Percentage(ins)})


def Library_Add_Books(request, cat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_cat = Master_catbook_data.objects.filter(ins = ins)
    form = AddBookForm()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    category = False
    if cat != 'ALL':
        category = Master_catbook_data.objects.filter(id = cat).first()
        if request.method == "POST":

            form = AddBookForm(request.POST,request.FILES)
            sub_cat = request.POST['subcategory']
            subcategory = Master_subcatbook_data.objects.filter(id = sub_cat).first()
            if form.is_valid():
                print("Is Valid")
                instance = form.save(commit=False)
                instance.category = category
                instance.subcategory = subcategory
                instance.created_date = format_date
                instance.ave_copy = instance.copies
                instance.ins = ins

                instance.save()
                return redirect('LibraryPanel:Library_book_List','All')

    return render(request,'Library/master_add_book.html',{"all_cat":all_cat,"category":category,"form":form,"adminprofile":Admin_data(),
                                                          "ins_data":Institute_data(request.user), 'isu':Issued_Percentage(ins)})

def Library_book_details(request, bid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    book =  Master_book_data.objects.filter(id=bid).first()
    return render(request,'Library/master_book_detail.html',{"book":book,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)})



def Library_Book_Edit_Details(request, bid,cat,subcat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_category = Master_catbook_data.objects.filter(ins = ins)
    data = Master_book_data.objects.filter(id=bid).first()
    data1 = Master_book_data.objects.filter(id=bid).first()
    category = Master_catbook_data.objects.filter(id = cat).first()
    subcategory =  Master_subcatbook_data.objects.filter(id = subcat).first()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    form = AddBookForm(instance=data)
    if request.method == "POST":
        form = AddBookForm(request.POST or None,request.FILES or None,instance=data)
        sub_cat = request.POST['subcategory']
        subcategory = Master_subcatbook_data.objects.filter(id=sub_cat).first()
        if form.is_valid():
            instance = form.save()
            instance.category = category
            instance.subcategory = subcategory
            instance.created_date = format_date

            copy = int(data1.copies)
            ava = int(data1.ave_copy)
            issued = copy - ava

            new_copy = int(instance.copies)

            if issued>=new_copy:
                new_copy = issued
                ava = 0
            else:
                ava = new_copy - issued
            instance.ave_copy = ava
            instance.copies = new_copy
            instance.save()

        return redirect("LibraryPanel:Library_book_details", bid)
    return render(request, "Library/master_add_book.html", {"form":form,'category':category,"all_cat":all_category,
                                                            "subcategory":subcategory,"dd":True, 'isu':Issued_Percentage(ins),
                                                            "bid":bid,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})

def Library_Online_Book(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_book = Master_E_Book.objects.filter(ins = ins)
    return render(request, 'Library/master_e_book.html',{"all_book":all_book, 'isu':Issued_Percentage(ins),"ins_data":Institute_data(request.user), "adminprofile":Admin_data()} )



def Library_E_Add_Books(request, cat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_cat = Master_catbook_data.objects.filter(ins = ins)
    form = AddEbookForm()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    category = False
    if cat != 'ALL':
        category = Master_catbook_data.objects.filter(id=cat).first()
        if request.method == "POST":

            form = AddEbookForm(request.POST, request.FILES)
            sub_cat = request.POST['subcategory']
            subcategory = Master_subcatbook_data.objects.filter(id=sub_cat).first()
            if form.is_valid():
                instance = form.save(commit=False)
                instance.category = category
                instance.subcategory = subcategory
                instance.created_date = format_date
                instance.ins = ins
                instance.save()
                return redirect('LibraryPanel:Library_online_book')
    return render(request, 'Library/master_add_e_book.html', {"all_category": all_cat, 'cat':category
                                                              ,"form":form,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)})

def Library_E_Book_Edit_Details(request, bid,cat,subcat):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_category = Master_catbook_data.objects.filter(ins = ins)
    data = Master_E_Book.objects.filter(id=bid).first()
    category = Master_catbook_data.objects.filter(id = cat).first()
    subcategory =  Master_subcatbook_data.objects.filter(id = subcat).first()
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')

    form = AddEbookForm(instance=data)
    if request.method == "POST":
        form = AddEbookForm(request.POST or None,request.FILES or None,instance=data)
        sub_cat = request.POST['subcategory']
        subcategory = Master_subcatbook_data.objects.filter(id=sub_cat).first()
        if form.is_valid():
            instance = form.save()
            instance.category = category
            instance.subcategory = subcategory
            instance.created_date = format_date
            instance.save()

        return redirect("LibraryPanel:Library_online_book")
    return render(request, "Library/master_add_e_book.html", {"form":form,'cat':category,"all_category":all_category,
                                                            "subcategory":subcategory,"dd":True, 'isu':Issued_Percentage(ins),
                                                            "bid":bid,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})


def Library_Online_Delete_Book(request, bid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_book = Master_E_Book.objects.filter(id = bid).first()
    all_book.delete()
    return redirect("LibraryPanel:Library_online_book")




def Filter_RollNumber(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    if request.method == 'POST':
        d = request.POST
        roll_number = d['roll_number']
        book_id = d['book_id']
        data = Front_student_data.objects.filter(ins = ins, roll_number = roll_number,status ='selected').first()
        if data:
         return redirect('LibraryPanel:Library_issue_book', data.id, book_id)

        else:
           return redirect('LibraryPanel:Library_book_List','error')




def Library_Book_Issue(request, student_data,bid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    ss = Front_student_data.objects.filter(id=student_data).first()
    dd = Library_Issue_Book.objects.filter(ins = ins, student = ss,status = 'Issued')
    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')

    if request.method == "POST":
        d = request.POST
        return_date = d['rdate']
        rdate = datetime.strptime(str(return_date), "%Y-%m-%d").strftime('%d/%m/%Y')
        book = Master_book_data.objects.filter(id =bid).first()
        if int(book.ave_copy) > 0:
            book.ave_copy = int(book.ave_copy)-1
            book.save()
            Library_Issue_Book.objects.create(ins = ins,student = ss,book=book,Due = rdate,
                                              status = 'Issued',issue = format_date,late_fee = 0)
        return redirect('LibraryPanel:Library_issued_book')


    return render(request, 'Library/master_issue_book.html',{"student_data":ss,"dd":dd,"issue_date":format_date, 'isu':Issued_Percentage(ins)
                                                             ,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})


def Library_Issued_Books(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    books = Library_Issue_Book.objects.filter(ins = ins, status = "Issued")
    return render(request, "Library/Issued_book.html", {'books':books,"ins_data":Institute_data(request.user), "adminprofile":Admin_data(), 'isu':Issued_Percentage(ins)})



def Library_Return_Book(request, bid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    book = Library_Issue_Book.objects.filter(id = bid).first()
    main_book = Master_book_data.objects.filter(id = book.book.id).first()
    main_book.ave_copy = int(main_book.ave_copy)+1
    main_book.save()
    today = date.today()
    format_date = datetime.strptime(str(today), "%Y-%m-%d").strftime('%d/%m/%Y')
    dt1 = book.Due.split('/')
    dt1.reverse()
    dt1 = ''.join(dt1)
    dt2 = format_date.split('/')
    dt2.reverse()
    dat = format_date
    dt2 = ''.join(dt2)
    dif = int(dt1)-int(dt2)
    data = LateFine.objects.filter(ins = ins).first()
    fine = 0
    if dif < 0:
        days = abs(dif)
        fine = days * int(data.libraryfine)
        book.status = "Fine"
        book.Return = dat
    else:
        book.status = "Returned"
        book.Return = dat
    book.late_fee = fine
    book.save()
    return redirect('LibraryPanel:Library_issued_book')

def Issue_Book_Return(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_book = Library_Issue_Book.objects.filter(ins = ins, status = 'Returned')
    return render(request,'Library/issue_book_return_list.html',{"books":all_book, 'isu':Issued_Percentage(ins),"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})

def Library_Student_Fine_List(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    data = Library_Issue_Book.objects.filter(ins = ins, status = 'Fine')
    li= []
    for i in data:
        li.append(int(i.late_fee))
    if request.method == "POST":
        d = request.POST
        book_id = d['book_id']
        stu_id = d['stu_id']
        fine = d['fine']
        
        #book = Master_book_data.objects.filter(id = book_id).first()
        #student = Front_student_data.objects.filter(id = stu_id).first()
        dd = Library_Issue_Book.objects.filter(id = stu_id).first()
        if int(dd.late_fee)== int(fine):
            dd.status = 'Returned'
            dd.late_fee = 0
            dd.save()
        else:
            dd.late_fee = int(dd.late_fee)-int(fine)
            dd.save()
        return redirect('LibraryPanel:Library_fine_list')
    return render(request,'Library/student_fine_list.html',{"data":data,"fine":li, 'isu':Issued_Percentage(ins),"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})

def Delete_for_all(request,num,type):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    if type == 'Category':
        data = Master_catbook_data.objects.filter(id = num).first()
        data.delete()

    if type == 'Subcategory':
        data = Master_subcatbook_data.objects.filter(id = num).first()
        data.delete()

    if type == 'Book':
        data = Master_book_data.objects.filter(id = num).first()
        data.delete()

    if type == 'Uncat_Book':
        data = Master_book_data.objects.filter(id=num).first()
        data.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def Uncategorized_books(request):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")
    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    books = Master_book_data.objects.filter(ins = ins, category = None,subcategory = None)
    li = []
    for bk in books:
        book = Master_book_data.objects.filter(id=bk.id).first()
        data = Library_Issue_Book.objects.filter(ins = ins, book=book, status='Issued')
        if data:
            li.append(bk)

    return render(request,'Library/uncategorized_books.html',{"books":books, 'isu':Issued_Percentage(ins),"li":li,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})

def Asign_category_to_book(request,cate,bid):
    if not request.user.is_authenticated():
        return redirect("login")
    user = request.user
    if not is_Librarian(user) and not is_admin(user):
        return redirect("login")

    ins = Institite_profile.objects.filter(id=int(user.first_name)).first()
    all_cat = Master_catbook_data.objects.filter(ins = ins)
    cat = False
    if cate != '0':
        cat = Master_catbook_data.objects.filter(id =cate).first()
        if request.method == "POST":
            d = request.POST
            sub_id = d['subcat']
            subcat = Master_subcatbook_data.objects.filter(id = sub_id).first()
            book = Master_book_data.objects.filter(id = bid).first()
            book.category = cat
            book.subcategory = subcat
            book.save()
            return redirect('LibraryPanel:Library_book_List', 'All')

    return render(request,'Library/asign_cat_to_book.html',{"all_cat":all_cat, 'isu':Issued_Percentage(ins),"cat":cat,"bid":bid,"ins_data":Institute_data(request.user), "adminprofile":Admin_data()})
