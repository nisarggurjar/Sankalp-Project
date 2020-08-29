from .models import *
from django import forms


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Master_book_data
        exclude = ('category','subcategory','created_date', 'ave_copy','ins')
        widgets = {
            "cover_image": forms.FileInput(attrs={ 'class': 'form-control'
                                                 }),
            "book_title": forms.TextInput(attrs={'placeholder': 'Book Title','class': 'form-control', "required": '',
                                             }),
            "subbook_title": forms.TextInput(attrs={'placeholder': 'Sub Title',
                                            'class': 'form-control', "required": ''}),
            "ISBN": forms.TextInput(attrs={'placeholder': 'ISBN',
                                         'class': 'form-control'}),
            "author": forms.TextInput(attrs={'placeholder': 'Author Name', 'class': 'form-control',
                                                 }),
            "publisher": forms.TextInput(attrs={'placeholder': 'Publisher Name',
                                                    'class': 'form-control'}),
            "editor": forms.TextInput(attrs={'placeholder': 'Editor Name',
                                          'class': 'form-control'}),
            "series": forms.TextInput(attrs={'placeholder': 'Series', 'class': 'form-control'
                                                 }),
            "publication_year": forms.TextInput(attrs={'placeholder': 'Publication Year',
                                                    'class': 'form-control'}),
            "edition": forms.TextInput(attrs={'placeholder': 'Edition',
                                          'class': 'form-control'}),
            "pages": forms.TextInput(attrs={'placeholder': 'Number Of Pages',
                                                    'class': 'form-control'}),
            "copies": forms.TextInput(attrs={'placeholder': 'Number Of Copies',
                                          'class': 'form-control', "required": ''}),

        }

class AddEbookForm(forms.ModelForm):
    class Meta:
        model = Master_E_Book
        exclude = ('category','subcategory','created_date','ins')
        widgets = {

            "book_title": forms.TextInput(attrs={'placeholder': 'Book Title','class': 'form-control', "required": '',
                                             }),

            "author": forms.TextInput(attrs={'placeholder': 'Author Nmae', 'class': 'form-control',
                                                 }),
            "publisher": forms.TextInput(attrs={'placeholder': 'Publisher Name',
                                                    'class': 'form-control',}),

            "book": forms.FileInput(attrs={'class': 'form-control', "required": ''}),

        }
