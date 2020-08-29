from django import forms
from .models import *

class SMS_Template_Form(forms.ModelForm):
    class Meta:
        model = SMSTemplate
        exclude = ()
        widgets = {
            "sender_id": forms.Select(attrs={'class': 'form-control show-tick', "required": '1',
                                          }),
            "title": forms.TextInput(attrs={'placeholder': 'Title',
                                           'class': 'form-control',"required":''}),
            "sms": forms.Textarea(attrs={'placeholder': 'Write your SMS', 'id':'mySMS',
                                            'class': 'form-control', "required": ''}),

        }

class AddEmployeForm(forms.ModelForm):
    class Meta:
        model = Master_employee_data
        exclude = ('created_date','designation', "ins")
        widgets = {

            "gender": forms.Select(attrs={'class': 'form-control show-tick', "required": '1',
                                               }),
            "name": forms.TextInput(attrs={'placeholder': 'Name',
                                           'class': 'form-control',"required":''}),
            "employee_id": forms.TextInput(attrs={'placeholder': 'Employee Id ',
                                           'class': 'form-control', "required": ''}),

            "email": forms.EmailInput(attrs={'placeholder': 'Email Id',
                                           'class': 'form-control', "required": ''}),
            "mobile": forms.NumberInput(attrs={'placeholder': 'Mobile Number',
                                           'class': 'form-control', "required": ''}),
            "qualification": forms.TextInput(attrs={'placeholder': 'Qualification',
                                           'class': 'form-control', "required": ''}),
            "university": forms.TextInput(attrs={'placeholder': 'University',
                                            'class': 'form-control', "required": ''}),
            "quali_year": forms.TextInput(attrs={'placeholder': 'Qualification year',
                                             'class': 'form-control', "required": ''}),
            "exp_year": forms.TextInput(attrs={'placeholder': 'Experiance',
                                           'class': 'form-control', "required": ''}),
            "discription_exp": forms.TextInput(attrs={'placeholder': 'Experiance Discription',
                                            'class': 'form-control'}),
            "address": forms.TextInput(attrs={'placeholder': 'Address',
                                             'class': 'form-control', "required": ''}),
            "dob": forms.DateInput(attrs={'placeholder': 'Date of Birth',
                                                    'class': 'form-control', "required": ''}),
            "aadhar_card": forms.NumberInput(attrs={'placeholder': 'Aadhar Number',
                                                 'class': 'form-control',
                                                  'maxlength': '12', 'size': '15'}),
            "join_date": forms.TextInput(attrs={'placeholder': 'Joining Date',
                                                 'class': 'form-control', "required": '',
                                                'maxlength': '10', 'size': '15'}),
            "office_in_time": forms.TextInput(attrs={'placeholder': 'Office In time',
                                               'class': 'form-control', "required": ''}),
            "office_out_time": forms.TextInput(attrs={'placeholder': 'office out time',
                                                     'class': 'form-control', "required": ''}),
            "resume": forms.FileInput(attrs={
                                              'class': 'form-control'}),
            "image": forms.FileInput(attrs={
                                             'class': 'form-control', "onchange":"readURL(this);"}),
            "salary":forms.TextInput(attrs={
                                             'class': 'form-control','placeholder': 'Enter salary', "required":"" }),

        }


class InstituteProfileForm(forms.ModelForm):
    class Meta:
        model = Institite_profile
        exclude = ('created_date','usr','map')
        widgets = {

            "name": forms.TextInput(attrs={'placeholder': 'Name',
                                           'class': 'form-control',"required":''}),
            "email": forms.TextInput(attrs={'placeholder': 'Email Id',
                                           'class': 'form-control', "required": ''}),
            "office_mob": forms.TextInput(attrs={'placeholder': 'Office Mobile Number',
                                           'class': 'form-control', "required": ''}),
            "office_add": forms.TextInput(attrs={'placeholder': 'Office Address',
                                           'class': 'form-control', "required": ''}),
            "landline_no": forms.TextInput(attrs={'placeholder': 'Office Landline Number',
                                            'class': 'form-control',}),
            "Title": forms.TextInput(attrs={'placeholder': 'Title',
                                             'class': 'form-control', "required": ''}),
            "sub_title": forms.TextInput(attrs={'placeholder': 'Sub Title',
                                           'class': 'form-control', "required": ''}),
            "website": forms.TextInput(attrs={'placeholder': 'Website Url',
                                            'class': 'form-control', "required": ''}),
            "state": forms.TextInput(attrs={'placeholder': 'State',
                                             'class': 'form-control', "required": ''}),
            "city": forms.TextInput(attrs={'placeholder': 'city',
                                                    'class': 'form-control', "required": ''}),
            "pan_number": forms.TextInput(attrs={'placeholder': 'Pan Number',
                                                 'class': 'form-control', "required": '',
                                                  }),
           "institute_logo": forms.FileInput(attrs={
                                             'class': 'form-control', "onchange":"readURL(this);", "required":""}),
           "institute_image": forms.FileInput(attrs={
                'class': 'form-control', "onchange": "readURL(this);", "required":""}),

        }




class Admin_profile_form(forms.ModelForm):
    class Meta:
        model = Admin_profile
        exclude = ('usr',)
        widgets = {

            "name": forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control',"required":''}),
            "email": forms.TextInput(attrs={'placeholder': 'Email Id', 'class': 'form-control', "required": ''}),
            "mobile": forms.TextInput(attrs={'placeholder': 'Mobile Number', 'class': 'form-control', "required": ''}),
            "address": forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control', "required": ''}),
            "dob": forms.TextInput(attrs={'placeholder': 'DOB', 'class': 'form-control', "required": ''}),
           "image": forms.FileInput(attrs={'class': 'form-control', "onchange":"readURL(this);"}),

        }


