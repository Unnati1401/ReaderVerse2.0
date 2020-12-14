from django import forms
from .models import UserProfileInfo,Institute

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter First Name',
    }),required=True)

    last_name = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Last Name',
    }),required=True)

    email = forms.CharField(widget = forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Email',
    }), required=True)

    username = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter username',
    }), required=True)

    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Enter password',
    }),required=True)

    phone = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter phone number',
    }),required=True)

    address = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter address',
    }), required=True)

    pincode = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter pincode',
    }),required=True)
    class Meta():
        model = UserProfileInfo
        exclude = ['latitude','longitude']


class InstituteSeekDonation(forms.ModelForm):
    #print("in instituteseekdonation")
    name = forms.CharField(widget = forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter Name Of School, NGO or Library',
    }),required=True)

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Email ID',
    }), required=True)

    contact = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter phone number',
    }), required=True)

    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Address',
    }), required=True)

    CHOICES = (
        ('Story Books', 'Story Books'),
        ('Novels', 'Novels'),
        ('Textbooks'),('Textbooks'),
        ('Magazines', 'Magazines'),
        ('Other','Other')
    )
    select= forms.CharField(widget=forms.Select(choices=CHOICES))

    Date = forms.DateField(widget=forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date','placeholder':'Enter date in YYYY-MM-DD'}), required=True)







    class Meta():
        model = Institute
        exclude = ['typebook','reqDate',]
