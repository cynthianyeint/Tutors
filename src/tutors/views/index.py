__author__ = 'Cynthia'

from django.shortcuts import render
from tutors.forms import TeacherRegister


def index(request):
    context = {
        'signup_form': TeacherRegister()
    }

    return render(request, 'tutors/index.html', context)


def about_us(request):
    context = {'about': "This is about page."}
    return render(request, 'tutors/about_us.html', context)
