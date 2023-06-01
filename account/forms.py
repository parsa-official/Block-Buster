from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
import os

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)	

class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()    
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    country = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=11)

class ChangeProfilePictureForm(forms.Form):
    profile_picture = forms.ImageField(label='Upload New Avatar:', required=False)
