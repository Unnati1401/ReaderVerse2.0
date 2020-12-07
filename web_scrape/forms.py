from django import forms

class BookForm(forms.Form):
    book = forms.CharField(label='Book', max_length=200)
