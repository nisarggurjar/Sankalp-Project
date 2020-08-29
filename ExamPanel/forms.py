from django.forms import ModelForm
from django import forms
from .models import *
from Institute.models import *
from ckeditor_uploader.fields import RichTextUploadingFormField

Ans = [
    ['1', '1'],
    ['2', '2'],
    ['3', '3'],
    ['4', '4'],
]

class DailyPracticeSubjectForm(forms.ModelForm):
    class Meta:
        model = DailyPracticeSubject
        exclude = ()
        widgets = {
            'course':forms.Select(attrs={
                                     'class': 'form-control show-tick',
                                          "required": ''
                                     }),
            'name': forms.TextInput(attrs={'placeholder': 'Subject Name', "class":"form-control","required": ''}),
            'logo': forms.FileInput(attrs={ "class":"form-control" }),
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ()
        widgets = {
            'package':forms.Select(attrs={
                                     'class': 'form-control show-tick',
                                          "required": ''
                                     }),
            'name': forms.TextInput(attrs={'placeholder': 'Topic Name', "class":"form-control",
                                           "required": ''}),

        }



class CreateExamPackageForm(forms.ModelForm):
    class Meta:
        model = ExamPackage
        exclude = ('status',)
        widgets = {
            'course':forms.Select(attrs={
                                     'class': 'form-control show-tick',
                                          "required": ''
                                     }),
            'name': forms.TextInput(attrs={'placeholder': 'Package Name', "class":"form-control","required": ''}),
            'fee': forms.TextInput(attrs={'placeholder': 'Package Fee', "value":"0","required": '',
                                          "class": "form-control"}),
            'o_fee': forms.TextInput(attrs={'placeholder': 'Fee for Other Student', "value": "0",
                                            "class": "form-control","required": ''}),
            'logo': forms.FileInput(attrs={ "class":"form-control" }),
            'syllabus': forms.FileInput(attrs={ "class":"form-control",})
        }


class CreateExamSubPackageForm(forms.ModelForm):
    class Meta:
        model = ExamSubPackage
        exclude = ('course',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Package Name', "class":"form-control"}),
        }


class CreateMainExamForm(forms.ModelForm):
    class Meta:
        model = MainExam
        exclude = ('course',)

        widgets = {
            'instruction':RichTextUploadingFormField(),
           # 'Sub_package':forms.Select(attrs={ 'class': 'form-control show-tick',"required": ''
            #                               }),
            'name': forms.TextInput(attrs={'placeholder': 'Exam Name', "class": "form-control", "required":""}),
            'start_date': forms.TextInput(attrs={'placeholder': 'Exam Start Date', "class": "form-control", "required":""}),
            'end_date': forms.TextInput(attrs={'placeholder': 'Exam End Date', "class": "form-control", "required":""}),
            'duration': forms.TextInput(attrs={'placeholder': 'Exam Duration ex. HH:MM',
                            "class":"form-control", "pattern":"([0-1]?[0-9]|2[0-4]):([0-5][0-9])", "required":""}),
            'syllabus': forms.FileInput(attrs={"class": "form-control"})

        }



class MultiChoiseQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestions
        exclude = ('section',
                   'explain2', 'explain3', 'explain4',
        'Type2', 'Question', 'Option1', 'Option2', 'Option3', 'Option4',
                   'Answer1', 'Answer2', 'Answer3', 'Answer4', 'marks2', 'minus2',
                   'Type3', 'Que', 'Answer31', 'Answer32', 'marks3', 'minus3',
                   'Type4', 'Ques_tion', 'TrueAns1', 'marks4', 'minus4')

        widgets = {
            'Questions': RichTextUploadingFormField(),
            'Option_1': RichTextUploadingFormField(),
            'Option_2': RichTextUploadingFormField(),
            'Option_3': RichTextUploadingFormField(),
            'Option_4': RichTextUploadingFormField(),
            'explain1': RichTextUploadingFormField(),

            'TrueAns': forms.Select(attrs={'class': 'form-control show-tick', "required": ''
                                               }),
            'marks1': forms.TextInput(attrs={'placeholder': '+Ve Mark', "class": "form-control", "required": ''}),
            'minus1': forms.TextInput(attrs={'placeholder': '+Ve Mark', "class": "form-control", "required": ''}),
            'Type1': forms.CheckboxInput(attrs={'checked': 'checked', 'hidden':""}),

        }



class MultiResponseQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestions
        exclude = ('section', 'explain1', 'explain3', 'explain4',
                   'Type1', 'Questions', 'Option_1',
                   'Option_2', 'Option_3', 'Option_4', 'TrueAns', 'marks1',
                   'minus1',
                   'Type3', 'Que', 'Answer31', 'Answer32', 'marks3', 'minus3',
                   'Type4', 'Ques_tion', 'TrueAns1', 'marks4', 'minus4')

        widgets = {
            'Question': RichTextUploadingFormField(),
            'Option1': RichTextUploadingFormField(),
            'Option2': RichTextUploadingFormField(),
            'Option3': RichTextUploadingFormField(),
            'Option4': RichTextUploadingFormField(),
            'explain2': RichTextUploadingFormField(),

            'Answer1': forms.CheckboxInput(),
            'Answer2': forms.CheckboxInput(),
            'Answer3': forms.CheckboxInput(),
            'Answer4': forms.CheckboxInput(),

            'marks2': forms.TextInput(attrs={'placeholder': '+Ve Mark', "class": "form-control", "required": ''}),
            'minus2': forms.TextInput(attrs={'placeholder': '-Ve Mark', "class": "form-control", "required": ''}),
            'Type2': forms.CheckboxInput(attrs={'checked': 'checked', 'hidden': ""}),


        }


class FillInTheBlankQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestions
        exclude = ('section', 'explain2', 'explain1', 'explain4',
                   'Type1', 'Questions', 'Option_1',
                   'Option_2', 'Option_3', 'Option_4', 'TrueAns', 'marks1',
                   'minus1',
                   'Type2', 'Question', 'Option1', 'Option2', 'Option3', 'Option4',
                   'Answer1', 'Answer2', 'Answer3', 'Answer4', 'marks2', 'minus2',

                   'Type4', 'Ques_tion', 'TrueAns1', 'marks4', 'minus4')

        widgets = {
            'Que': RichTextUploadingFormField(),
            'explain3': RichTextUploadingFormField(),
            'Answer31': forms.TextInput(attrs={'placeholder': 'Correct Answer', "class": "form-control"}),
            'Answer32': forms.TextInput(attrs={'placeholder': 'Correct Answer (Optional)', "class": "form-control"}),
            'marks3': forms.TextInput(attrs={'placeholder': '+Ve Mark', "class": "form-control", "required": ''}),
            'minus3': forms.TextInput(attrs={'placeholder': '-Ve Mark', "class": "form-control", "required": ''}),
            'Type3': forms.CheckboxInput(attrs={'checked': 'checked', 'hidden': ""}),
        }



class TrueFalseQuestionForm(forms.ModelForm):
    class Meta:
        model = MultipleChoiceQuestions
        exclude = ('section', 'explain2', 'explain3', 'explain1',
                   'Type1', 'Questions', 'Option_1',
                   'Option_2', 'Option_3', 'Option_4', 'TrueAns', 'marks1',
                   'minus1',
                   'Type2', 'Question', 'Option1', 'Option2', 'Option3', 'Option4',
                   'Answer1', 'Answer2', 'Answer3', 'Answer4', 'marks2', 'minus2',
                   'Type3', 'Que', 'Answer31', 'Answer32', 'marks3', 'minus3'
                   )

        widgets = {
            'Ques_tion': RichTextUploadingFormField(),
            'explain4': RichTextUploadingFormField(),
            'TrueAns1': forms.Select(attrs={'class': 'form-control show-tick', "required": ''
                                           }),
            'marks4': forms.TextInput(attrs={'placeholder': '+Ve Mark', "class": "form-control", "required": ''}),
            'minus4': forms.TextInput(attrs={'placeholder': '-Ve Mark', "class": "form-control", "required": ''}),
            'Type4': forms.CheckboxInput(attrs={'checked': 'checked', 'hidden': ""}),

        }



class CreateQuizPackageForm(forms.ModelForm):
    class Meta:
        model = QuizPackage
        exclude = ('status',)
        widgets = {
            'course':forms.Select(attrs={
                                     'class': 'form-control show-tick',
                                          "required": ''
                                     }),
            'name': forms.TextInput(attrs={'placeholder': 'Package Name', "class":"form-control"
                                           , "required": ''}),
            'fee': forms.TextInput(attrs={'placeholder': 'Package Name', "value":"0",
                                          "class": "form-control", "required": ''}),
            'logo': forms.FileInput(attrs={ "class":"form-control" }),
            'syllabus': forms.FileInput(attrs={ "class":"form-control"})
        }





class AddNewStudentForm(forms.ModelForm):
    class Meta:
        model = Add_New_Student
        exclude = ("usr",)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Student Name', "class":"form-control", "required": ''}),
            'father_name': forms.TextInput(attrs={'placeholder': 'Father Name', "class":"form-control"}),
            'dob': forms.DateInput(attrs={'placeholder': 'Date of Birth', "class":"form-control", "required": ''}),
            'gender': forms.Select(attrs={ "class":"form-control show-tick", "required": ''}),
            'mobile': forms.NumberInput(attrs={'placeholder': 'Mobile Number', "class":"form-control", "required": '',
                                               "oninput": "javascript: if (this.value.length > 10) this.value = this.value.slice(0, 10);",
                                               }),
            'college': forms.TextInput(attrs={'placeholder': 'College/University Name', "class":"form-control", "required": ''}),
            'pursuing': forms.TextInput(attrs={'placeholder': 'Current Education', "class":"form-control", "required": ''}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email ID', "class":"form-control", "required": ''}),
            'photo': forms.FileInput(attrs={"class":"form-control", "id":"photo", "onchange":"fileValidation2(this.id)", "required": ''}),
            'id_proof': forms.FileInput(attrs={"class":"form-control", "id":"identy", "onchange":"fileValidation2(this.id)", "required": ''}),

        }
