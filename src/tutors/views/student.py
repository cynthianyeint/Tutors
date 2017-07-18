from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from tutors.models import Student, UserProfile, Teacher
from tutors.permission import in_student_group

__author__ = 'Cynthia'


@user_passes_test(in_student_group, login_url=reverse_lazy('user-login'))
def student_dashboard(request, **kwargs):

    if request.user.id is not None:
        user_id = request.user.id
        student = get_object_or_404(Student, user__id=user_id)
        # if not request.user.social_auth.filter(provider='facebook') and not request.user.social_auth.filter(provider='google-oauth2'):
        #     if not student.user_activated:
        #         resend_activation_url = reverse('resend-activation', kwargs={'user_id': user_id})
        #         messages.warning(request, 'Your account has not been activated, yet. Please check your email and activate to fully utilize all the features.<br/>Didn\'t get it? <a href="' + resend_activation_url + '">Resend Now.</a>')

        if request.GET.get('tab', ''):
            active_tab = request.GET.get('tab', '')
        else:
            active_tab = "profile"

    return render(request, 'tutors/student/profile.html', {'student': student, 'active_tab': active_tab})


def teacher_view(request, **kwargs):
    teacher_id = kwargs.get('pk', '')
    teacher = Teacher.objects.filter(pk=teacher_id).first()

    return render(request, 'tutors/student/teacher-view.html', {'teacher_id': teacher_id, 'teacher': teacher})


def student_view(request, **kwargs):
    student_id = kwargs.get('pk', '')
    student = Student.objects.filter(pk=student_id).first()

    return render(request, 'tutors/teacher/student-view.html', {'student_id': student_id, 'student': student})