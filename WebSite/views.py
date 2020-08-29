from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from .models import *
from Institute.models import *
# Create your views here.
from datetime import datetime,date
def DirectorProfile():
    data = Director_Profile.objects.filter().first()
    return data
def Counter():
    data = Counter_data.objects.filter().first()
    return data
def AllBrands():
    data = Brands.objects.all()
    return data
    
def Website_home(request):
    banners = Banner.objects.all()
    all_course = Main_course.objects.all()
    all_sub_course = Sub_course.objects.all()
    all_ins = Institite_profile.objects.all()
    all_feedback = Faculty_Feddback.objects.all()
    welcome_content = Welcome_content.objects.filter().first()
    return render(request,'web/index.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"banners":banners,"all_course":all_course
                                            ,"all_ins":all_ins,"all_feedback":all_feedback,
                                            "all_sub_course":all_sub_course,"welcome_content":welcome_content})

def Student_quiry_form(request):
    if request.method == "POST":
        d = request.POST
        name = d['name']
        mobile = d['mob']
        email = d['email']
        center_id = d['center']
        course_id =d['course']
        message = d['msg']
        course = Sub_course.objects.filter(id = course_id).first()
        center = Institite_profile.objects.filter(id = center_id).first()
        Student_Query.objects.create(institute = center,course = course,name = name,
                                     mobile = mobile,email = email,message = message)
        return redirect(request.META.get('HTTP_REFERER'))
def Website_admin_login(request):

    error = False
    if request.method == "POST":
        u = request.POST['user']
        p = request.POST['pwd']
        user = authenticate(username = u,password = p)
        if user:
            login(request,user)
            return redirect('website_home')
        else:
            error = True

    return render(request,'web/web_login.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"error":error})

def Website_admin_logout(request):
    logout(request)
    return redirect('website_home')


def Website_slider_add(request):
    all_course = Main_course.objects.all()
    if request.method == "POST":
        s = request.FILES['slider']
        mh = request.POST['head']
        sh = request.POST['subhead']
        Banner.objects.create(slider = s,head = mh,subhead=sh)
        return redirect('website_home')
    return render(request,'web/web_add_slider.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_course":all_course})

def Website_slider_delete(request,sid):

    data = Banner.objects.filter(id = sid).first()
    data.delete()
    return redirect('website_home')


def Website_add_course(request):
    all_course = Main_course.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        dis = request.POST['dis']
        Main_course.objects.create(name = name,dis = dis)
        return redirect('website_home')
    return render(request,'web/web_add_course.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_course":all_course})

def Website_add_subcourse(request,mid):
    all_course = Main_course.objects.all()
    data = Main_course.objects.filter(id = mid).first()
    if request.method == "POST":
        img = request.FILES['img']
        name = request.POST['name']
        dis = request.POST['dis']
        fee = request.POST['fee']
        Sub_course.objects.create(main_course = data,image = img,name = name,dis = dis,fee = fee)
        return redirect('website_home')
    return render(request,'web/web_add_subcourse.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_course":all_course,"data":data})



def Main_course_details(request,mid):
    all_course = Main_course.objects.all()
    data = Main_course.objects.filter(id = mid).first()
    return render(request,'web/main_course_details.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"data":data,"all_course":all_course})


def Sub_course_details(request,sid):
    all_course = Main_course.objects.all()
    data = Sub_course.objects.filter(id = sid).first()
    related_course = Sub_course.objects.filter(main_course = data.main_course)
    content = Course_content.objects.filter(sub_course = data)
    return render(request,'web/sub_course_details.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"data":data,"all_course":all_course
                                                         ,"related_course":related_course
                                                         ,"content":content})


def AboutUs(request):
    all_course = Main_course.objects.all()
    about_content = About_Us_content.objects.filter().first()
    return render(request,'web/about_us.html',{"brand":AllBrands(),"counter":Counter(),
                                               "profile":DirectorProfile(),"all_course":all_course
                                               ,"about_content":about_content})

def ContactUs(request):
    all_course = Main_course.objects.all()
    all_sub_course = Sub_course.objects.all()
    all_center = Institite_profile.objects.all()
    return render(request,'web/contact_us.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_course":all_course,"all_sub_course":all_sub_course
                                                 ,"all_center":all_center})


def Branches(request):
    all_course = Main_course.objects.all()
    all_branch = Institite_profile.objects.all()

    return render(request,'web/branches.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_branch":all_branch,"all_course":all_course
                                               })


def Student_Zone(request):
    ids = []
    all_course = Main_course.objects.all()
    institutes = Institite_profile.objects.all()
    upcoming_batch = []
    today_date = date.today()
    format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
    date_split = format_date.split('/')
    date_reverse = date_split[3::-1]
    Tdate = int(''.join(date_reverse))
    for i in institutes:
      all_batch = Master_batch_data.objects.filter(ins=i)
      for batch in all_batch:
            ##### Start Date make As a Number #######

            startDate = batch.start_date
            d_split = startDate.split('/')
            d_reverse = d_split[3::-1]
            Sdate =  int(''.join(d_reverse))

            if Sdate>=Tdate:
                ids.append(i.id)
                upcoming_batch.append(batch)
    print(upcoming_batch)

    return render(request,'web/student_zone.html',{"brand":AllBrands(),"counter":Counter(),"profile":DirectorProfile(),"all_course":all_course,"upcoming_batch":upcoming_batch
                                                   ,"institutes":institutes,"ids":ids})




def Change_profile(request,type):
    all_course = Main_course.objects.all()
    data = DirectorProfile()
    if type == "Image":
        if request.method == "POST":
            image = request.FILES['image']
            data.image = image
            data.save()
            return redirect('website_home')
    if type == "Details":
        if request.method == "POST":
            d = request.POST
            data.name = d['name']
            data.mobile_number = d['mob']
            data.address = d['add']
            data.email = d['email']
            data.director_message = d['msg']

            data.save()
            return redirect('website_home')

    return render(request,'web/change_profile.html',{"brand":AllBrands(),"counter":Counter(),"profile":data,"all_course":all_course})

def Delete_stuff(request,type,num):
    if type == 'MainCourse':
        data = Main_course.objects.filter(id = num).first()
        data.delete()
    if type == 'SubCourse':
        data = Sub_course.objects.filter(id = num).first()
        cid = data.main_course.id
        data.delete()
        return redirect('Website:main_cdetails',cid)
    if type == 'Brand':
        data = Brands.objects.filter(id = num).first()
        data.delete()
    if type == 'Review':
        data = Student_Feedback.objects.filter(id = num).first()
        data.delete()

    if type == 'Faculty':
        data = Faculty_Feddback.objects.filter(id = num).first()
        data.delete()

    if type == 'Gallery':
        data = Our_gallery_data.objects.filter(id = num).first()
        data.delete()

    if type == 'Content':
        data = Course_content.objects.filter(id = num).first()
        data.delete()

    return redirect(request.META.get("HTTP_REFERER"))


def Edit_Main_course(request,num):
    all_course = Main_course.objects.all()
    data = Main_course.objects.filter(id = num).first()
    if request.method == "POST":
        d = request.POST
        data.name = d['name']
        data.dis = d['dis']
        data.save()
        return redirect('website_home')

    return render(request,'web/edit_maincourse.html',{"brand":AllBrands(),"counter":Counter(),"data":data,"profile":DirectorProfile(),"all_course":all_course})

def Edit_Welcome_content(request,type):
    all_course = Main_course.objects.all()
    data = Welcome_content.objects.filter().first()
    if request.method == "POST":
        c = request.POST['content']
        if type == "First_Content":
            data.content = c
            data.save()
            return redirect('website_home')

        if type == "Second_Content":
            data.why_choose = c
            data.save()
            return redirect('website_home')

    return render(request,'web/edit_welcome_content.html',{"brand":AllBrands(),"counter":Counter(),"data":data,
                                                       "profile":DirectorProfile(),
                                                       "all_course":all_course,"type":type})

def Add_Review(request):
    all_course = Main_course.objects.all()
    all_subcourse = Sub_course.objects.all()
    if request.method == "POST":
        c = request.POST['cid']
        course = Sub_course.objects.filter(id = c).first()
        name = request.POST['name']
        feedback = request.POST['review']
        image = request.FILES['img']
        Student_Feedback.objects.create(name = name,sub_course = course,feedback = feedback,image= image)
        return redirect('website_home')

    return render(request, 'web/add_review.html', {"brand": AllBrands(), "counter": Counter(),
                                                             "profile": DirectorProfile(),
                                                             "all_course": all_course,"all_subcourse":all_subcourse})


def Add_Faculty_Review(request):
    all_course = Main_course.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        feedback = request.POST['review']
        image = request.FILES['img']
        Faculty_Feddback.objects.create(name = name,feedback = feedback,image= image)
        return redirect('website_home')

    return render(request, 'web/add_faculty_review.html', {"brand": AllBrands(), "counter": Counter(),
                                                             "profile": DirectorProfile(),
                                                             "all_course": all_course})



def Add_brand(request):
    all_course = Main_course.objects.all()
    if request.method == "POST":
        image = request.FILES['img']
        Brands.objects.create(image = image)
        return redirect('website_home')
    return render(request, 'web/add_brand.html', {"brand": AllBrands(), "counter": Counter(),
                                                   "profile": DirectorProfile(),
                                                   "all_course": all_course})



def Edit_counter(request):
    data = Counter()
    all_course = Main_course.objects.all()
    if request.method == "POST":
        d = request.POST
        data.value1 = d['value1']
        data.value2 = d['value2']
        data.value3 = d['value3']
        data.value4 = d['value4']
        data.save()
        return redirect('website_home')
    return render(request, 'web/edit_counter.html', {"brand": AllBrands(), "counter": Counter(),
                                                  "profile": DirectorProfile(),
                                                  "all_course": all_course})

def Edit_About_Content(request,type):
    data = About_Us_content.objects.filter().first()
    all_course = Main_course.objects.all()
    if request.method == "POST":
        c = request.POST['content']
        if type == "Who_we_are":
            data.who_we_are = c
            data.save()

        elif type == "Why_join_us":
            data.why_join_us = c
            data.save()

        elif type == "Our_vision":
            data.our_vision = c
            data.save()

        elif type == "Our_mission":
            data.our_mission = c
            data.save()

        elif type == "Mission_tag_line":
            data.mission_tag_line = c
            data.save()
        return redirect('Website:aboutus')

    return render(request, 'web/edit_about_content.html', {"brand": AllBrands(), "counter": Counter(),
                                                     "profile": DirectorProfile(),
                                                     "all_course": all_course,"data":data,"type":type})


def Change_image(request,option):
    data = About_Us_content.objects.filter().first()
    data2 = Welcome_content.objects.filter().first()
    all_course = Main_course.objects.all()
    if request.method == "POST":
        c = request.FILES['image']
        if option == "Who_we_are":
            data.image1 = c
            data.save()
            return redirect('Website:aboutus')

        elif option == "Why_join_us":
            data.image2 = c
            data.save()
            return redirect('Website:aboutus')

        elif option == "Welcome_content":
            data2.image = c
            data2.save()
            return redirect('website_home')



    return render(request, 'web/change_image.html', {"brand": AllBrands(), "counter": Counter(),
                                                           "profile": DirectorProfile(),
                                                           "all_course": all_course, "data": data, "type": option,
                                                           "data2":data2})


def Student_Reviews(request):
    all_course = Main_course.objects.all()
    all_feedback = Student_Feedback.objects.all()
    return render(request,'web/student_review.html', {"brand": AllBrands(), "counter": Counter(),
                                                           "profile": DirectorProfile(),
                                                           "all_course": all_course,"all_feedback":all_feedback })


def Our_gallery(request):
    all_course = Main_course.objects.all()
    data = Our_gallery_data.objects.all()
    return render(request,'web/our_gallery.html',{"brand": AllBrands(), "counter": Counter(),
                                                           "profile": DirectorProfile(),
                                                           "all_course": all_course,"data":data})


def Add_Gallery(request):
    all_course = Main_course.objects.all()
    if request.method == "POST":
        c = request.FILES['image']
        t = request.POST['title']
        Our_gallery_data.objects.create(image = c,Title= t)
        return redirect('Website:add_galley')

    return render(request, 'web/add_gallery.html', {"brand": AllBrands(), "counter": Counter(),
                                                    "profile": DirectorProfile(),
                                                    "all_course": all_course})



def Edit_sub_course(request,type,num):
    all_course = Main_course.objects.all()
    data = Sub_course.objects.filter(id = num).first()
    if type == "Image":
        if request.method == "POST":
            image = request.FILES['image']
            data.image = image
            data.save()
            return redirect('Website:sub_cdetails',num)
    if type == "Details":
        if request.method == "POST":
            d = request.POST
            dd = Main_course.objects.filter(id = d['cid']).first()
            data.main_course = dd
            data.name = d['name']
            data.dis = d['dis']
            data.fee = d['fee']
            data.long_dis = d['long_dis']

            data.save()
            return redirect('Website:sub_cdetails',num)

    return render(request, 'web/edit_subcourse_details.html',
                  {"brand": AllBrands(), "counter": Counter(),
                   "profile": DirectorProfile(), "all_course": all_course
                   ,"data":data})


def Edit_course_content(request,num):
    all_course = Main_course.objects.all()
    data = Course_content.objects.filter(id = num).first()
    if request.method == "POST":
        d = request.POST
        data.heading = d['heading']
        data.content = d['dis']
        data.save()
        return redirect('Website:sub_cdetails',data.sub_course.id)

    return render(request, 'web/edit_content.html',
                  {"brand": AllBrands(), "counter": Counter(),
                   "profile": Director_Profile, "all_course": all_course
                      , "data": data})

def Add_content(request,num):
    all_course = Main_course.objects.all()
    data = Sub_course.objects.filter(id = num).first()
    if request.method == "POST":
        d = request.POST
        heading = d['heading']
        content = d['dis']
        Course_content.objects.create(sub_course = data,heading = heading,content=content)
        return redirect('Website:sub_cdetails', data.id)

    return render(request, 'web/add_content.html',
                  {"brand": AllBrands(), "counter": Counter(),
                   "profile": DirectorProfile(), "all_course": all_course
                      })


def Add_sub_course(request,num):
    all_course = Main_course.objects.all()
    data = Main_course.objects.filter(id=num).first()
    if request.method == "POST":
        d = request.POST
        name = d['name']
        dis = d['dis']
        long_dis = d['long_dis']
        fee = d['fee']
        image = request.FILES['image']
        Sub_course.objects.create(main_course = data,name = name,dis= dis,long_dis = long_dis
                                  ,image = image,fee = fee)
        return redirect('Website:main_cdetails',data.id)
    return render(request, 'web/add_sub_course.html',
                  {"brand": AllBrands(), "counter": Counter(),
                   "profile": DirectorProfile(), "all_course": all_course
                   ,"data":data})













