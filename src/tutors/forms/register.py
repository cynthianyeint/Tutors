import datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import *
from django.forms.extras import SelectDateWidget
from tutors.models import Teacher, TITLE_CHOICES, Student

__author__ = 'Cynthia'


class NewUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_email_exist = User.objects.filter(email=email).count() > 0
        if email and is_email_exist:
            raise forms.ValidationError(u'This email address is already registered.')
        return email


class EditUserForm(UserChangeForm):
    email = forms.EmailField(required=True, label="Email address")

    class Meta:
        model = User
        fields = ('email', )

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(u'This email address is already registered.')
        return email


class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('title', 'first_name', 'last_name', 'nickname', 'dob', 'website', 'mobile_number', 'home_phone_number', 'biography')
        exclude = ['user', 'private_birthyear']

    last_name = forms.CharField(required=False)
    dob = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1900, datetime.datetime.now().year+1)],  attrs=({'style': 'width: 32.5%; display: inline-block;'})),required=False, label='Date of Birth')
    title = forms.ChoiceField(choices=TITLE_CHOICES, widget=forms.RadioSelect())


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('title', 'first_name', 'last_name', 'dob', 'mobile_number', 'home_phone_number')
        exclude = ['user']

    title = forms.ChoiceField(choices=TITLE_CHOICES, widget=forms.RadioSelect())
    last_name = forms.CharField(required=False)
    dob = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1900, datetime.datetime.now().year+1)], attrs=({'style': 'width: 32.5%; display: inline-block;'})),required=False, label='Date of Birth')


class TeacherRegister(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Password'}))
