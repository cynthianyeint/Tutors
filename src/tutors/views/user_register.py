from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group, User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from social.pipeline import social_auth
from tutors.models import Teacher, UserActivation, UserProfile, Student
from tutors.permission import in_teacher_group, group_check
from tutors.user import generate_and_send_activation_email
from django.shortcuts import render, get_object_or_404
from tutors.forms import NewUserRegisterForm, TeacherRegisterForm, EditUserForm, UserProfileForm, StudentRegisterForm, \
    ChangePasswordForm

__author__ = 'Cynthia'


def user_register(request):
    return render(request, 'tutors/user_register/user_register.html')


def teacher_register_form(request, teacher_id=None):
    context = {}
    message = ''
    user_profile_form = ''
    if teacher_id:
        is_new = False
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        if teacher and teacher.user and teacher.user_id:
            existing_user = get_object_or_404(User, pk=teacher.user_id)
        else:
            existing_user = None
            # todo: raise error + log error
            pass
    else:
        is_new = True
        teacher = Teacher()
        existing_user = User()

    if request.POST:
        if teacher_id:
            user_form = EditUserForm(request.POST, instance=existing_user, prefix="userform")
            user_profile = UserProfile.objects.filter(user=existing_user).first()
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            user_form = NewUserRegisterForm(request.POST, instance=existing_user, prefix="userform")

        teacher_register_form = TeacherRegisterForm(request.POST, instance=teacher, prefix="teacherform")

        if user_profile_form:
            if user_profile_form.is_valid():
                user_profile_form_save = user_profile_form.save(commit=False)
                user_profile_form_save.user = existing_user
                delete_avatar = user_profile_form.data.get('avatar-clear', '')
                if delete_avatar == 'on':
                    user_profile.delete()
                else:
                    user_profile_form_save.save()

        if user_form.is_valid() and teacher_register_form.is_valid():
            # try: # don't suppress real (bug) errors
            teacher_form = teacher_register_form.save(commit=False)
            new_user = user_form.save(commit=False)
            email = user_form.cleaned_data['email']

            new_user.username = email
            new_user.is_active = True
            new_user.save()
            try:
                group = Group.objects.get(name='Teacher')
                group.user_set.add(new_user)
            except Exception, ex:
                User.objects.filter(pk=new_user.id).delete()
                message = "%s %s" % ("You cannot add as a teacher.", "Please contact the admin.")
                messages.warning(request, message)
                return HttpResponseRedirect(reverse('teacher-user-register'))

            teacher_form.user = new_user
            teacher_form.save()

            # generate_and_send_activation_email(new_user)

            return HttpResponseRedirect(reverse('activation-sent'))

            # if request.user.is_authenticated() and request.user.groups.filter(name="Teacher"):
            #     return HttpResponseRedirect(reverse('teacher_dashboard'))
            # todo: what happens in `else`?

    else:  # method is not POST
        if teacher_id:
            user_form = EditUserForm(instance=existing_user, prefix="userform")
            user_profile = UserProfile.objects.filter(user=existing_user).first()
            user_profile_form = UserProfileForm(instance=user_profile)
        else:
            user_form = NewUserRegisterForm(instance=existing_user, prefix="userform")

        teacher_register_form = TeacherRegisterForm(instance=teacher, prefix="teacherform")

    if message:
        message = message

    context['is_new'] = is_new
    context['user_form'] = user_form
    context['teacher_register_form'] = teacher_register_form
    context['user_profile_form'] = user_profile_form
    context['message'] = message
    return render(request, 'tutors/user_register/teacher_register_form.html', context)


def activation_sent(request):
    context = {}
    return render(request, 'tutors/user_register/activation_sent.html', context)


def resend_activation(request, **kwargs):
    context = {}
    user_id = kwargs.get('user_id')
    if user_id:
        if request.method == "POST":
            user = User.objects.filter(pk=user_id).first()
            # generate_and_send_activation_email(user)
            return HttpResponseRedirect(reverse('activation-sent'))
        else:
            context['user_id'] = user_id
            get_user_activation = UserActivation.objects.filter(user=user_id).first()
            if get_user_activation.is_activated:
                is_teacher = Teacher.objects.filter(user=user_id).first()
                if is_teacher:
                    return HttpResponseRedirect(reverse('teacher_dashboard'))
                else:
                    return HttpResponseRedirect(reverse('student_dashboard'))

        return render(request, 'tutors/user_register/resend_activation.html', context)
    return HttpResponseRedirect(reverse('user-login'))


def student_register_form(request, student_id = None):
    context = {}
    user_profile_form = ''

    if student_id:
        is_new = False
        student = get_object_or_404(Student,pk=student_id)
        if student and student.user and student.user_id:
            existing_user = get_object_or_404(User, pk=student.user_id)
    else:
        is_new = True
        existing_user = User()
        student = Student()

    if request.POST:
        if student_id:
            user_form = EditUserForm(request.POST, instance=existing_user, prefix="userform")
            user_profile = UserProfile.objects.filter(user=existing_user).first()
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        else:
            user_form = NewUserRegisterForm(request.POST, instance=existing_user, prefix="userform")

        student_register_form = StudentRegisterForm(request.POST, instance=student, prefix="studentform")

        if user_profile_form:
            if user_profile_form.is_valid():
                user_profile_form_save = user_profile_form.save(commit=False)
                user_profile_form_save.user = existing_user
                delete_avatar = user_profile_form.data.get('avatar-clear', '')
                if delete_avatar == 'on':
                    user_profile.delete()
                else:
                    user_profile_form_save.save()

        if user_form.is_valid() and student_register_form.is_valid():
            student_form = student_register_form.save(commit=False)
            new_user = user_form.save(commit=False)
            email = user_form.cleaned_data['email']

            new_user.username = email
            new_user.is_active = True
            new_user.save()

            group = Group.objects.get(name='Student')
            group.user_set.add(new_user)

            student_form.user = new_user
            student_form.save()

            # generate_and_send_activation_email(new_user)

            return HttpResponseRedirect(reverse('activation-sent'))
    else:
        if student_id:
            user_form = EditUserForm(instance=existing_user, prefix="userform")
            user_profile = UserProfile.objects.filter(user=existing_user).first()
            user_profile_form = UserProfileForm(instance=user_profile)
        else:
            user_form = NewUserRegisterForm(instance=existing_user, prefix="userform")

        student_register_form = StudentRegisterForm(instance=student, prefix="studentform")

    context['is_new'] = is_new
    context['user_form'] = user_form
    context['user_profile_form'] = user_profile_form
    context['student_register_form'] = student_register_form
    return render(request, 'tutors/user_register/student_register_form.html', context)


@user_passes_test(group_check, login_url=reverse_lazy('user-login'))
def user_edit_password(request, **kwargs):
    user_id = kwargs.get('user_id', '')
    user = get_object_or_404(User, pk=user_id)
    if request.POST:
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            try:
                change_password = form.save(commit=False)
                change_password.save()

                return HttpResponseRedirect(reverse('teacher_dashboard'))

            except Exception, ex:
                message = "Error: %s" % ex.message

        else:
            message = "Form is not valid. Please try again."

    else:
        form = ChangePasswordForm(instance=user)
    return render(request, 'tutors/user_register/change_password.html', {'form': form})


def social_login_group(request, string=None):
    if string:
        get_user = request.user
        if string == "teacher":
            group_name = "Teacher"
            register_obj = Teacher()
            success_redirect_url = "teacher_dashboard"
            err_redirect_url = "teacher-user-register"
        else:
            group_name = "Student"
            register_obj = Student()
            success_redirect_url = "student_dashboard"
            err_redirect_url = "student-register"
        try:
            is_user_in_group = is_in_multiple_groups(get_user, "Teacher", "Student")
            if not is_user_in_group:
                group = Group.objects.get(name=group_name)
                group.user_set.add(get_user)
                register_obj.first_name = get_user.first_name
                register_obj.last_name = get_user.last_name
                register_obj.user_id = get_user.id
                register_obj.save()
                return HttpResponseRedirect(reverse(success_redirect_url))
            else:
                raise Exception
        except Exception, ex:
            message = "You cannot add as a %s. Please contact the admin." % string
            messages.warning(request, message)
            return HttpResponseRedirect(reverse(err_redirect_url))


def is_in_multiple_groups(user, teacher, student):
    return user.groups.filter(name__in=[teacher, student]).exists()