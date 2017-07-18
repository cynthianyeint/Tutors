from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from tutors.forms import UserLoginForm
from tutors.models import UserActivation
from django.contrib.auth import logout as auth_logout

__author__ = 'Cynthia'


def get_username(email):
    try:
        user = User.objects.filter(email=email.lower()).first()
        return user
    except User.DoesNotExist:
        return None

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_login(request):
    err_message = ""
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = get_username(email)
        user = authenticate(username=username, password=password)
        form = UserLoginForm(request.POST, request.FILES, instance=user)
        if user is not None:
            login(request, user)
            #return HttpResponseRedirect(reverse('home'))
            if request.user.groups.filter(name="Teacher"):
                return HttpResponseRedirect(reverse('teacher_dashboard'))
            elif request.user.groups.filter(name="Student"):
                return HttpResponseRedirect(reverse('student_dashboard'))
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            err_message = "Email and/or Password incorrect."
    else:
        form = UserLoginForm
    return render(request, 'tutors/user_login/user_login.html', {"form": form, "message": err_message})


def user_activated_confirm(request, activation_key):
    activation_date = timezone.now()
    is_activated = True
    try:
        user_activated = get_object_or_404(UserActivation, activation_key=activation_key)
        user_activated.activation_date = activation_date
        user_activated.is_activated = is_activated
        user_activated.save()
        message = "Your account has been successfully activated."

    except Exception, ex:
        message = "Sorry. Cannot activated. Please contact Admin."
    return render(request, "tutors/user_register/activation.html", {"message": message})


def social_login(request):
    user = request.user
    if user is not None:
        if user.groups.filter(name="Teacher"):
            return HttpResponseRedirect(reverse('teacher_dashboard'))
        elif user.groups.filter(name="Student"):
            return HttpResponseRedirect(reverse('student_dashboard'))
        else:
            return HttpResponseRedirect(reverse('home'))


def social_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

