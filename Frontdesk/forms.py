
from .models import *
from django import forms
from datetime import date,datetime

class Student_form(forms.ModelForm):
    class Meta:
        model = Front_student_data

        exclude = ('status','roll_number','id_card_validity', "usr", 'ins')
        widgets = {
            "name": forms.TextInput(attrs={'placeholder': 'Name',
                                           'class': 'form-control',
                                           "required":''}),

            "image": forms.FileInput(attrs={'class': 'form-control',
                                            "onchange":"readURL(this);"}),
            "dob": forms.TextInput(attrs={'placeholder': 'Date of Birth',
                                           'class': 'form-control'
                                          ,"required":'','maxlength':'10','size':'15'
                                          }),
            "address": forms.TextInput(attrs={'placeholder': 'Address',
                                          'class': 'form-control'
                                              ,"required":''}),
            "mobile": forms.NumberInput(attrs={'placeholder': 'Mobile Number', "oninput":"javascript: if (this.value.length > 10) this.value = this.value.slice(0, 10);",
                                          'class': 'form-control',
                                             "required": ''}),
            "email": forms.EmailInput(attrs={'placeholder': 'Email Address',
                                          'class': 'form-control',
                                            "required": ''}),
            "college": forms.TextInput(attrs={'placeholder': 'College/School',
                                          'class': 'form-control',
                                              }),
            "graduation": forms.TextInput(attrs={'placeholder': 'Graduation/Standard',
                                          'class': 'form-control',
                                                 }),

            "gender": forms.Select(attrs={'name': 'gender',
                                     'class': 'form-control show-tick',
                                          "required": ''
                                     }),
            "stream": forms.TextInput(attrs={'placeholder': 'Stream/Subject',
                                                 'class': 'form-control',

                                                 }),
            "Father_name": forms.TextInput(attrs={'placeholder': 'Father\'s name',
                                             'class': 'form-control'
                                             }),
            "father_mob": forms.TextInput(attrs={'placeholder': 'Father\'s Contact No.',
                                                  'class': 'form-control'
                                                  }),
            "father_add": forms.TextInput(attrs={'placeholder': 'Father\'s Address',
                                                  'class': 'form-control'
                                                  }),
            "Occupation": forms.TextInput(attrs={'placeholder': 'Father\'s Occupation',
                                                  'class': 'form-control'
                                                  }),



        }



class Enquiry_form(forms.ModelForm):
    class Meta:
        model = Front_enquiry_data
        today_date = date.today()
        format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
        exclude = ('visited_date','status','course', "ins",'follow_up_time','course_name')
        widgets = {

            "student_name": forms.TextInput(attrs={'placeholder': 'Name',
                                           'class': 'form-control',"required":'1'}),
            "father_name": forms.TextInput(attrs={'placeholder': 'Fathers\'name',
                                                   'class': 'form-control'}),

            "address": forms.TextInput(attrs={'placeholder': 'Address',
                                              'class': 'form-control',"required":'1'}),

            "mobile": forms.NumberInput(attrs={'placeholder': 'Mobile Number', "oninput":"javascript: if (this.value.length > 10) this.value = this.value.slice(0, 10);",
                                             'class': 'form-control',"required":'1'}),

            "email": forms.EmailInput(attrs={'placeholder': 'Email Address',
                                            'class': 'form-control',"required":'1'}),

            "college": forms.TextInput(attrs={'placeholder': 'College/School',
                                              'class': 'form-control'}),

            "graduation": forms.TextInput(attrs={'placeholder': 'Graduation/Standard',
                                                 'class': 'form-control'
                                                 }),


            "remark": forms.TextInput(attrs={'placeholder': 'Remark',
                                             'class': 'form-control',"required":'1'
                                             }),

            "follow_up_date": forms.TextInput(attrs={'placeholder': 'Follow Up Date',
                                                  'class': 'form-control',"required":'1',
                                                  'maxlength':'10','size':'15', 'minlength':'10'
                                                  }),


    }

class Call_log_form(forms.ModelForm):
    class Meta:
        model = Front_call_logs
        today_date = date.today()
        format_date = datetime.strptime(str(today_date), "%Y-%m-%d").strftime('%d/%m/%Y')
        exclude = ('call_date','ins','course','follow_up_time')
        widgets = {

            "student_name": forms.TextInput(attrs={'placeholder': 'Name',
                                           'class': 'form-control',"required":'1'}),
            "next_follow_up_date": forms.TextInput(attrs={'placeholder': 'Next Follow Up Date',
                                                   'class': 'form-control', "required": '1'
                                                          ,"maxlength":'10',"size":'15'}),
            "remark": forms.TextInput(attrs={'placeholder': 'Remark',
                                              'class': 'form-control',"required":'1'}),

            "mobile": forms.TextInput(attrs={'placeholder': 'Mobile Number',
                                             'class': 'form-control',"required":'1'}),

               }

