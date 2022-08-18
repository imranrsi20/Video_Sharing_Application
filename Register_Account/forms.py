from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'first name'}),
                                 required=True, max_length=20)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'last name'}),
                                required=True, max_length=20)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your E-mail'}), required=True,
        max_length=50)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}),
                               required=True, max_length=25)


    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
                               required=True, max_length=50)
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={ 'placeholder': 'confirm password'}), required=True,
        max_length=50)

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email','username', 'password1', 'password2' )



    def clean_username(self):
        user=self.cleaned_data['username']
        try:
            match=User.objects.get(username=user)
        except:
            return self.cleaned_data['username']
        raise forms.ValidationError('username alrady exist')
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            match=User.objects.get(email=email)
        except:
            return self.cleaned_data['email']
        raise forms.ValidationError('email already exist')





class C_channel(forms.ModelForm):
    channel_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True,max_length=1000)

    class Meta:
        model=author
        fields=[
            'channel_name',
            'profile_picture',
            'channel_background_image'
        ]
