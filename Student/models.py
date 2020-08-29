from django.db import models
from Frontdesk.models import *



class Student_add_link(models.Model):
    student = models.ForeignKey(Front_student_data,on_delete=models.CASCADE,null=True)
    facebook_link = models.CharField(max_length=500,null=True,blank=True)
    twitter_link = models.CharField(max_length=500, null=True, blank=True)
    instagram_link = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.student.name