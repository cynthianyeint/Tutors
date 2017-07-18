# from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from tutors.models import Teacher, Class, DAY_CHOICES, ClassCategory, Student
from tutors.permission import in_teacher_group
from tutors.forms import get_time_choices
from datetime import time


__author__ = 'Cynthia'


@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def teacher_dashboard(request):

    if request.user.id is not None:
        # teacher = Teacher.objects.get(user__id=request.user.id)
        user_id = request.user.id
        teacher = get_object_or_404(Teacher, user__id=user_id)
        course_list = Class.enabled_objects.filter(teacher=teacher).annotate(count_student=Count('student'))
        total_course = course_list.count
        total_student = 0
        for c in course_list:
            total_student += c.count_student if c.count_student else 0
        # if not request.user.social_auth.filter(provider='facebook') and not request.user.social_auth.filter(provider='google-oauth2'):
        #     if not teacher.user_activated:
        #         resend_activation_url = reverse('resend-activation', kwargs={'user_id': user_id})
        #         messages.warning(request, 'Your account has not been activated, yet. Please check your email and activate to fully utilize all the features.<br/>Didn\'t get it? <a href="' + resend_activation_url + '">Resend Now.</a>')

        # notification = request.user.notifications.all()

        if request.GET.get('tab', ''):
            active_tab = request.GET.get('tab', '')
        else:
            active_tab = "profile"

        return render(request, 'tutors/teacher/profile.html', {'teacher': teacher, 'total_course': total_course, 'total_students': total_student, 'course_list': course_list, 'active_tab': active_tab})


class SearchList(ListView):
    model = Teacher
    context_object_name = 'result_list'
    template_name = "tutors/search/tutor_search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        context['int_list'] = DAY_CHOICES
        context['time_list'] = get_time_choices()
        context['class_cat_list'] = ClassCategory.objects.all()
        return context

    def get_queryset(self, **kwargs):
        return filter_search_list(self)


def filter_search_list(self):
    custom_search = self.request.GET.get('custom_search', '')
    nick_name = self.request.GET.get('search_nick_name', '')
    website = self.request.GET.get('search_website', '')
    first_name = self.request.GET.get('search_first_name', '')
    last_name = self.request.GET.get('search_last_name', '')
    class_title = self.request.GET.get('search_class_title', '')
    class_category = self.request.GET.get('search_class_category_name', '')
    description = self.request.GET.get('search_description', '')
    int_day = self.request.GET.get('search_int_day', '')
    from_time = self.request.GET.get('search_from_time', '')
    to_time = self.request.GET.get('search_to_time', '')
    from_date = self.request.GET.get('search_from_date', '')
    to_date = self.request.GET.get('search_to_date', '')

    result = Class.objects.select_related('teacher')
    if custom_search:
        result = result.filter(Q(teacher__nickname__icontains=custom_search) |
                               Q(teacher__website__icontains=custom_search) |
                               Q(teacher__first_name__icontains=custom_search) |
                               Q(teacher__last_name__icontains=custom_search) |
                               Q(title__icontains=custom_search) |
                               Q(description__icontains=custom_search))

    if nick_name:
        result = result.filter(teacher__nickname__icontains=nick_name)
    if website:
        result = result.filter(teacher__website__icontains=website)
    if first_name:
        result = result.filter(teacher__first_name__icontains=first_name)
    if last_name:
        result = result.filter(teacher__last_name__icontains=last_name)
    if class_title:
        result = result.filter(title__icontains=class_title)
    if class_category:
        result = result.filter(category__id=class_category)
    if description:
        result = result.filter(description__icontains=description)
    if int_day:
        result = result.filter(classschedule__timeslot__int_day=int_day)
    if from_date:
        result = result.filter(class_event__occurrence__start_time__gte=from_date)
    if to_date:
        result = result.filter(class_event__occurrence__end_time__lte=to_date)
    if from_date and to_date:
        result = result.filter(class_event__occurrence__start_time__gte=from_date, class_event__occurrence__end_time__lte=to_date)

    if from_time:
        from_time = from_time.split(":")
        result = result.filter(class_event__occurrence__start_time__hour=from_time[0],class_event__occurrence__start_time__minute=from_time[1])
    if to_time:
        to_time = to_time.split(":")
        result = result.filter(class_event__occurrence__end_time__hour=to_time[0], class_event__occurrence__end_time__minute=to_time[1])

    if from_time and to_time:
        result = result.filter(class_event__occurrence__start_time__hour=from_time[0],
                               class_event__occurrence__start_time__minute=from_time[1],
                               class_event__occurrence__end_time__hour=to_time[0],
                               class_event__occurrence__end_time__minute=to_time[1])

    # if from_time:
    #     result = result.filter(classschedule__timeslot__from_time=from_time)
    # if to_time:
    #     result = result.filter(classschedule__timeslot__to_time=to_time)

    return result.distinct()
