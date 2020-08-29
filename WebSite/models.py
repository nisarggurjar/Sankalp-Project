from django.db import models
from Institute.models import *
# Create your models here.

class Banner(models.Model):
    slider = models.FileField(null=True,blank=True)
    head = models.CharField(max_length=100,null=True,blank=True)
    subhead = models.CharField(max_length=200,null=True,blank=True)


class Main_course(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    dis = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

class Sub_course(models.Model):
    main_course = models.ForeignKey(Main_course,models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    image = models.FileField(null=True, blank=True)
    dis = models.CharField(max_length=200, null=True, blank=True)
    long_dis = models.CharField(max_length=2000, null=True, blank=True)
    fee = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.main_course.name + ' -> ' + self.name

class Course_content(models.Model):
    sub_course = models.ForeignKey(Sub_course, models.CASCADE, null=True)
    heading = models.CharField(max_length=200,null=True,blank=True)
    content = models.TextField(null=True,blank=True)


class Student_Feedback(models.Model):
    sub_course = models.ForeignKey(Sub_course,on_delete=models.CASCADE,null=True)
    image = models.FileField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

class Student_Query(models.Model):
    institute = models.ForeignKey(Institite_profile,on_delete=models.CASCADE,null=True)
    course = models.ForeignKey(Sub_course,on_delete=models.CASCADE,null=True)
    name =  models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=13, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(null=True, blank=True)


class Director_Profile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    director_message = models.TextField(null=True, blank=True)


class Welcome_content(models.Model):
    image = models.FileField(null=True, blank=True)
    content = models.TextField(null=True,blank=True)
    why_choose = models.TextField(null=True,blank=True)

class About_Us_content(models.Model):
    who_we_are = models.TextField(null=True,blank=True)
    image1 = models.FileField(null=True, blank=True)
    why_join_us = models.TextField(null=True,blank=True)
    image2 = models.FileField(null=True, blank=True)
    our_vision = models.TextField(null=True,blank=True)
    our_mission = models.TextField(null=True,blank=True)
    mission_tag_line = models.CharField(max_length=100, null=True, blank=True)

class Counter_data(models.Model):
    value1 = models.IntegerField(null=True, blank=True)
    value2 = models.IntegerField(null=True, blank=True)
    value3 = models.IntegerField(null=True, blank=True)
    value4 = models.IntegerField(null=True, blank=True)



class Brands(models.Model):
    image = models.FileField(null=True, blank=True)

class Faculty_Feddback(models.Model):
    image = models.FileField(null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)


class Our_gallery_data(models.Model):
    image = models.FileField(null=True)
    Title = models.CharField(max_length=100,null=True)












