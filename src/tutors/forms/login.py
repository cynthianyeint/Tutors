from tutors.models import UserProfile

__author__ = 'Cynthia'

from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('email', 'password')


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, label="Profile Image")

    class Meta:
        model = UserProfile
        fields = ('avatar', )
