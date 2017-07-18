from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from notifications.models import Notification
from tutors.models import Teacher, Student, Application, Class
from tutors.permission import group_check

__author__ = 'Cynthia'


@user_passes_test(group_check, login_url=reverse_lazy('user-login'))
def course_application(request, id=None):
    total_course = ''
    if id:
        application = Application.objects.filter(pk=id).first()
        course_list = Class.enabled_objects.filter(pk=application.course.id)
        total_course = course_list.count

        # mark notification as read for student
        if request.user.groups.filter(name="Student"):
            notification = get_object_or_404(Notification, recipient=application.student.user, target_object_id=id)
            notification.mark_as_read()

        # if not application.teacher.user_activated or application.student.user_activated:
        #     resend_activation_url = reverse('resend-activation', kwargs={'user_id': request.user.id})
        #     messages.warning(request, 'Your account has not been activated, yet. Please check your email and activate to fully utilize all the features.<br/>Didn\'t get it? <a href="' + resend_activation_url + '">Resend Now.</a>')

    return render(request, 'tutors/applications/application.html', {'application': application, 'total_course': total_course})


@user_passes_test(group_check, login_url=reverse_lazy('user-login'))
def pending_applications(request):

    if request.user.groups.filter(name="Teacher"):
        user = Teacher.objects.filter(user__id=request.user.id).first()
    else:
        user = Student.objects.filter(user__id=request.user.id).first()
    # if not request.user.social_auth.filter(provider='facebook') and not request.user.social_auth.filter(provider='google-oauth2'):
    #     if not user.user_activated:
    #         resend_activation_url = reverse('resend-activation', kwargs={'user_id': request.user.id})
    #         messages.warning(request, 'Your account has not been activated, yet. Please check your email and activate to fully utilize all the features.<br/>Didn\'t get it? <a href="' + resend_activation_url + '">Resend Now.</a>')

    return render(request, 'tutors/applications/pending_applications.html', {'user': user})