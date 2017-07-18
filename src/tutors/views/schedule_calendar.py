__author__ = 'Cynthia'

import calendar
import itertools
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from swingtime.models import Event, Occurrence
from swingtime import utils
from tutors.models import Class
from django.contrib.auth.decorators import user_passes_test
from tutors.permission import in_teacher_group
from django.core.urlresolvers import reverse_lazy
from swingtime.forms import EventForm, MultipleOccurrenceForm, SingleOccurrenceForm
from django.http import HttpResponseRedirect
from dateutil import parser


def _datetime_view(request, template, dt,course_id, timeslot_factory=None, items=None, params=None):

    timeslot_factory = timeslot_factory or utils.create_timeslot_table
    params = params or {}

    course = Class.objects.filter(id=course_id).first()

    return render(request, template, {
        'course': course,
        'course_id': course_id,
        'day':       dt,
        'next_day':  dt + timedelta(days=+1),
        'prev_day':  dt + timedelta(days=-1),
        'timeslots': timeslot_factory(dt, items, **params)
    })


def day_view(request, year, month, day, course_id, template='swingtime/daily_view.html', **params):
    dt = datetime(int(year), int(month), int(day))
    course_id = course_id
    return _datetime_view(request, template, dt, course_id, **params)

def course_month_view(request, **kwargs):
    # queryset = None
    year = int(kwargs.get('year', ''))
    month = int(kwargs.get('month', ''))
    course_id = kwargs.get('course_id', '')

    occurrences = Occurrence.objects.filter(start_time__year=year, start_time__month=month)
    if request.user.groups.filter(name="Teacher"):
        event_id = []
        course = Class.objects.filter(teacher__user_id=request.user.id)
        for c in course:
            event_id.append(c.class_event_id)

        occurrences = occurrences.filter(event_id__in=event_id)
    else:
        occurrences = occurrences

    data = monthly_data(course_id, year, month, occurrences)
    return render(request, 'swingtime/monthly_view.html', data)


def monthly_data(course_id, year, month, occurrences):

    cal = calendar.monthcalendar(year, month)
    dtstart = datetime(year, month, 1)
    last_day = max(cal[-1])
    dtend  = datetime(year, month, last_day)

    def start_day(o):
        return o.start_time.day

    by_day = dict([(dt, list(o)) for dt,o in itertools.groupby(occurrences, start_day)])
    data = {
        'course_id': course_id,
        'today':      datetime.now(),
        'calendar':   [[(d, by_day.get(d, [])) for d in row] for row in cal],
        'this_month': dtstart,
        'next_month': dtstart + timedelta(days=+last_day),
        'last_month': dtstart + timedelta(days=-1),
    }
    return data


@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def schedule_view(request, course_id=None, event_id=None):
    if course_id:
        course = Class.objects.filter(pk=course_id).first()
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
        event_form = recurrence_form = None
        if request.POST:
            if '_update' in request.POST:
                event_form = EventForm(request.POST, instance=event)
                if event_form.is_valid():
                    event_form.save(event)
                    return HttpResponseRedirect(request.path)
            elif '_add' in request.POST:
                recurrence_form = MultipleOccurrenceForm(request.POST)
                if recurrence_form.is_valid():
                    recurrence_form.save(event)
                    return HttpResponseRedirect(request.path)
            else:
                pass
        else:
            if 'dtstart' in request.GET:
                dtstart = parser.parse(request.GET.get('dtstart', ''))
            else:
                dtstart = datetime.now()

            event_form = EventForm(instance=event)
            recurrence_form = MultipleOccurrenceForm(initial={'dtstart':dtstart, 'until': dtstart})

        return render(request, 'swingtime/event_detail.html', {'course_id': course_id, 'course': course, 'event': event,'event_form': event_form, 'recurrence_form': recurrence_form, 'dtstart':dtstart})


@user_passes_test(in_teacher_group, login_url=reverse_lazy('user-login'))
def occurrence_view(request, **kwargs):
    event_id = kwargs.get('event_id', '')
    occurrence_id = kwargs.get('occurrence_id', '')

    occurrence = get_object_or_404(Occurrence, pk=occurrence_id, event__pk=event_id)
    course = get_object_or_404(Class, class_event__pk=event_id)
    if request.POST:
        form = SingleOccurrenceForm(request.POST, instance=occurrence)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = SingleOccurrenceForm(instance=occurrence)

    return render(request, 'swingtime/occurrence_detail.html', {'occurrence': occurrence, 'form':form, 'course_id':course.id})
