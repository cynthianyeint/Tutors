from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

__author__ = 'Cynthia'


class ChangePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password1', 'password2')