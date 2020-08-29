from __future__ import unicode_literals

from django.db import models
from Frontdesk.models import *
from Institute.models import *
# Create your models here.
class Master_catbook_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.name

class Master_subcatbook_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Master_catbook_data,models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.CharField(max_length=20, null=True, blank=True)


    def __str__(self):
        return self.name

class Master_book_data(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True,blank=True)
    cover_image = models.FileField(null=True,blank=True)
    category = models.ForeignKey(Master_catbook_data,on_delete=models.SET_NULL,null=True, blank=True)
    subcategory = models.ForeignKey(Master_subcatbook_data,on_delete=models.SET_NULL,null=True, blank=True)
    book_title = models.CharField(max_length=100, null=True, blank=True)
    subbook_title = models.CharField(max_length=100, null=True, blank=True)
    ISBN = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    editor = models.CharField(max_length=100, null=True, blank=True)
    series = models.CharField(max_length=100, null=True, blank=True)
    publication_year = models.CharField(max_length=100, null=True, blank=True)
    edition = models.CharField(max_length=100, null=True, blank=True)
    pages = models.CharField(max_length=100, null=True, blank=True)
    copies = models.CharField(max_length=100, null=True, blank=True)
    ave_copy = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.book_title

class Master_E_Book(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Master_catbook_data,on_delete= models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Master_subcatbook_data, on_delete=models.SET_NULL, null=True, blank=True)
    book_title = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    book = models.FileField(null=True, blank=True)
    created_date = models.CharField(max_length=100, null=True, blank=True)




class Library_Issue_Book(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Master_book_data, on_delete=models.CASCADE)
    student = models.ForeignKey(Front_student_data, on_delete=models.CASCADE)
    issue = models.CharField(max_length=50, null=True, blank=True)
    Due = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    Return = models.CharField(max_length=50, null=True, blank=True)
    late_fee = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.student.name + " / " + self.book.book_title




class LateFine(models.Model):
    ins = models.ForeignKey(Institite_profile, on_delete=models.CASCADE, null=True)
    libraryfine = models.CharField(max_length=20, null=True, blank=True)
    latefeefine = models.CharField(max_length=20, null=True, blank=True)
