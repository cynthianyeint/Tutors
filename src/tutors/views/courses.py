from django.forms import modelformset_factory
from tuition.settings import COURSE_IMAGE_URL, COURSE_IMAGE_DIR, COURSE_IMAGE_EXTRA, COURSE_IMAGE_MAX

__author__ = 'Cynthia'

from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from tutors.forms import CourseForm, ImageForm
from django.views.generic import ListView, DetailView
from tutors.models import Class, Teacher, CourseImageUpload
from tutors.permission import in_teacher_group, group_check
from datetime import datetime
from dateutil import parser
from swingtime.forms import EventForm, MultipleOccurrenceForm
from swingtime.models import Occurrence
from schedule_calendar import monthly_data
from django.db.models import Count


class CoursesListView(ListView):
    model = Class
    context_object_name = 'course_list'
    template_name = 'tutors/courses/list.html'

    def dispatch(self, *args, **kwargs):
        return super(CoursesListView, self).dispatch(*args, **kwargs)

    def get_queryset(self, **kwargs):

        if self.request.GET.get('search'):
            id = self.request.GET.get('id', '')
            course_list = Class.objects.filter(pk=id)
        else:
            course_list = Class.objects.all()

        return course_list

    def get_context_data(self, **kwargs):
        context = {}
        context = super(CoursesListView, self).get_context_data(**kwargs)
        course_list = context['course_list']
        popular_course_list = course_list.annotate(recommend_count=Count('recommendation')).order_by('-recommend_count')
        newest_course_list = course_list.order_by('-id')
        context['popular_course_list'] = popular_course_list
        context['newest_course_list'] = newest_course_list
        return context


class CoursesDetailView(DetailView):
    model = Class
    context_object_name = 'course'
    template_name = 'tutors/courses/detail.html'

    def dispatch(self, *args, **kwargs):
        return super(CoursesDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        today = datetime.now()

        # year = today.year
        # month = today.month
        # course_id = context['course'].id

        if self.request.GET.get('year',''):
            year = int(self.request.GET.get('year', ''))
        else:
            year = today.year

        if self.request.GET.get('month', ''):
            month = int(self.request.GET.get('month', ''))
        else:
            month = today.month

        course_id = context['course'].id

        occurrences = Occurrence.objects.filter(start_time__year=year, start_time__month=month,event=context['course'].class_event)
        data = monthly_data(course_id, year, month, occurrences)

        context['monthly_data'] = data

        context['img_list'] = CourseImageUpload.objects.filter(class_obj=course_id)
        return context

def get_class_recommend():
    pass
# @user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
# def create_course(request, id = None):
#
#     return_url = request.GET.get('next', '')
#     existing_course = existing_time_slot = None
#     title_text = "Add Course"
#     title_icon = "plus-square"
#     existing_time_slot_count = 0
#     exist_time_slot = None
#     existing_list_time_slot = []
#     if id:
#         existing_course = Class.enabled_objects.get(pk=id)
#         exsiting_class_schedule = ClassSchedule.objects.filter(cls=existing_course)
#         existing_time_slot = TimeSlot.objects.filter(schedule=exsiting_class_schedule)
#         title_text = "Edit Course"
#         title_icon = "pencil-square"
#
#     if request.POST:
#         course_form = CourseForm(request.POST, instance=existing_course)
#         timeslot_form = ClassTimeSlotForm(request.POST)
#
#         int_day_list = request.POST.getlist('int_day')
#         from_time_list = request.POST.getlist('from_time')
#         to_time_list = request.POST.getlist('to_time')
#
#         if course_form.is_valid() and timeslot_form.is_valid():
#             course = course_form.save(commit=False)
#
#             teacher_user = Teacher.objects.filter(user__id=request.user.id).first()
#             if teacher_user is not None:
#                 course.teacher = teacher_user
#             course.save()
#
#             if existing_course is not None and exsiting_class_schedule:
#                 class_schedule = ClassSchedule.objects.filter(cls=existing_course).first()
#             else:
#                 class_schedule = ClassSchedule()
#                 class_schedule.cls = course
#                 class_schedule.save()
#
#             for index, value in enumerate(int_day_list):
#                 if id:
#                     timeslot_id = []
#                     for e in existing_time_slot:
#                         timeslot_id.append(e.pk)
#                     TimeSlot.objects.filter(pk__in=timeslot_id).delete()
#
#                 TimeSlot(from_time=from_time_list[index], to_time=to_time_list[index], schedule=class_schedule, int_day=value).save()
#
#             # return HttpResponseRedirect(reverse('teacher_dashboard'))
#                 return HttpResponseRedirect(return_url)
#         else:
#             existing_time_slot_count = len(int_day_list)
#             for index, value in enumerate(int_day_list):
#                 existing_list_time_slot.append([int_day_list[index], str(from_time_list[index]), str(to_time_list[index])])
#             exist_time_slot = base64.b64encode(json.dumps(existing_list_time_slot))
#
#     else:
#         if existing_course:
#             course_form = CourseForm(instance=existing_course)
#             existing_time_slot_count = existing_time_slot.count()
#             for i in existing_time_slot:
#                 existing_list_time_slot.append([i.int_day, str(i.from_time), str(i.to_time)])
#             exist_time_slot = base64.b64encode(json.dumps(existing_list_time_slot))
#         else:
#             course_form = CourseForm()
#
#         timeslot_form = ClassTimeSlotForm()
#
#     return render(request, 'tutors/teacher/add_course.html', {'days': DAY_CHOICES, 'course_form': course_form, 'existing_time_slot': existing_time_slot,
#                                                               'title_text': title_text, 'title_icon': title_icon, 'timeslot_form': timeslot_form,
#                                                               'existing_time_slot_count': existing_time_slot_count, "exist_time_slot": exist_time_slot})

@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def create_course(request, id=None):
    # return_url = request.GET.get('next', '')
    title_text = "Add Course"
    title_icon = "plus-square"
    existing_course = None
    ImageFormSet = modelformset_factory(CourseImageUpload, form=ImageForm, extra=COURSE_IMAGE_EXTRA, max_num=COURSE_IMAGE_MAX)
    if id:
        title_text = "Edit Course"
        title_icon = "pencil-square"
        existing_course = Class.enabled_objects.get(pk=id)

    if request.POST:
        # formset = ImageFormSet(request.POST, request.FILES,
        #                        queryset=CourseImageUpload.objects.filter(class_obj=existing_course.id))
        # course_img_files = request.FILES.getlist('files', None)

        course_form = CourseForm(request.POST, instance=existing_course)

        if course_form.is_valid() :
            course = course_form.save(commit=False)

            teacher_user = Teacher.objects.filter(user__id=request.user.id).first()
            if teacher_user is not None:
                course.teacher = teacher_user
            course.save()

            # Save course image files
            # if course_img_files:
            #     upload_course_image_files(course_img_files, course.id)
            # for form in formset.cleaned_data:
            #     images = form.get('images', None)
            #     if images:
            #         is_img_exists = CourseImageUpload.objects.filter(class_obj=course, images=images).first()
            #         if not is_img_exists:
            #             photo = CourseImageUpload(class_obj=course, images=images)
            #             photo.save()
            # return HttpResponseRedirect(return_url)
            return HttpResponseRedirect(reverse('course-details', kwargs={'course_id': course.id}))
    else:
        if existing_course:
            course_form = CourseForm(instance=existing_course)
            # formset = ImageFormSet(queryset=CourseImageUpload.objects.filter(class_obj=existing_course.id))
        else:
            course_form = CourseForm()
            # formset = ImageFormSet(queryset=CourseImageUpload.objects.none())
    # return render(request, 'tutors/courses/add_course.html', {'course_form': course_form, 'title_text': title_text, 'title_icon': title_icon, 'formset': formset})
    return render(request, 'tutors/courses/add_course.html', {'course_form': course_form, 'title_text': title_text, 'title_icon': title_icon})


# def upload_course_image_files(image_list, course_id):
#     for count, x in enumerate(image_list):
#         def process(f):
#             with open(COURSE_IMAGE_URL+"/"+f.name, 'wb+') as destination:
#                 for chunk in f.chunks():
#                     destination.write(chunk)
#             class_obj = Class.objects.filter(pk=course_id).first()
#             CourseImageUpload(class_obj=class_obj, images=COURSE_IMAGE_DIR+"/"+f.name).save()
#         process(x)


@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def add_course_schedule(request, course_id=None):
    start_date = ""
    dtstart = ""
    if course_id:
        course = Class.objects.filter(pk=course_id).first()
    if request.POST:
        event_form = EventForm(request.POST)
        recurrence_form = MultipleOccurrenceForm(request.POST)
        if event_form.is_valid() and recurrence_form.is_valid():
            event = event_form.save()

            course.class_event = event
            course.save()

            recurrence_form.save(event)

            return HttpResponseRedirect(reverse('course-schedule_view', kwargs={'course_id': course_id,'event_id': event.id}))
    else:
        if 'dtstart' in request.GET:
            start_date = parser.parse(request.GET.get('dtstart',''))
        else:
            start_date = datetime.now()

        dtstart = start_date
        event_form = EventForm
        recurrence_form = MultipleOccurrenceForm(initial={'dtstart': dtstart, 'until': dtstart})

    return render(request, 'swingtime/add_event.html', {'id': id, 'dtstart': dtstart, 'event_form': event_form, 'recurrence_form': recurrence_form, 'course_id': course_id})


@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def delete_course(request, id=None):
    if id:
        course = Class.objects.filter(pk=id).first()
        course.enabled = False
        course.save()
        return HttpResponseRedirect(reverse('teacher_dashboard'))
    return render(request, 'tutors/courses/delete.html')


@user_passes_test(group_check, login_url=reverse_lazy('user-login'))
def course_details(request, course_id=None):
    teacher = ""
    if course_id:
        course = Class.enabled_objects.get(pk=course_id)
        student_list = course.student.all()

        if request.user.id is not None and request.user.groups.filter(name="Teacher"):
            user_id = request.user.id
            teacher = get_object_or_404(Teacher, user__id=user_id)

    today = datetime.now()

    if request.GET.get('year',''):
        year = int(request.GET.get('year', ''))
    else:
        year = today.year

    if request.GET.get('month', ''):
        month = int(request.GET.get('month', ''))
    else:
        month = today.month

    occurrences = Occurrence.objects.filter(start_time__year=year, start_time__month=month, event_id=course.class_event_id)
    data = monthly_data(course_id, year, month, occurrences)

    if request.user.groups.filter(name="Teacher"):
        return render(request, 'tutors/teacher/course-detail.html', {'teacher': teacher, 'course': course, 'student_list': student_list, 'monthly_data': data})
    else:
        return render(request, 'tutors/student/course-detail.html', {'teacher': teacher, 'course': course, 'student_list': student_list, 'monthly_data': data})


# def course_image_list(request):
#     CourseImageUpload.objects.filter(class_obj_id=)