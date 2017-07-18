from datetime import time
from django.forms import ModelForm, ModelChoiceField, ChoiceField, Select
from tutors.models import Class, ClassCategory, TimeSlot, DAY_CHOICES

__author__ = 'Cynthia'


def get_time_choices():
    count = 8
    time_list = ()
    time_list += (('', '-------'),)
    while count <= 20:
        time_list += ((str(time(count, 00, 00)), str(count) + ':00'),)
        time_list += ((str(time(count, 15, 00)), str(count) + ':15'),)
        time_list += ((str(time(count, 30, 00)), str(count) + ':30'),)
        time_list += ((str(time(count, 45, 00)), str(count) + ':45'),)
        count += 1
    return time_list


class CourseForm(ModelForm):

    class Meta:
        model = Class
        fields = ('title', 'description', 'category', 'published', 'youtube_link')

    category = ModelChoiceField(queryset=ClassCategory.objects.all())


class ClassTimeSlotForm(ModelForm):
    class Meta:
        model = TimeSlot
        fields = ('int_day', 'from_time', 'to_time')

    int_day = ChoiceField(choices=DAY_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super(ClassTimeSlotForm, self).__init__(*args, **kwargs)
        self.fields['from_time'] = ChoiceField(choices=get_time_choices(), widget=Select(attrs={'class': 'from_time_slot', 'required': 'required'}))
        self.fields['to_time'] = ChoiceField(choices=get_time_choices(), widget=Select(attrs={'class': 'to_time_slot', 'required': 'required'}))

    def clean(self):
        get_from_time = self.data.getlist('from_time')
        get_to_time = self.data.getlist('to_time')
        if get_from_time and get_to_time:
            for f_key, f_value in enumerate(get_from_time):
                for t_key, t_value in enumerate(get_to_time):
                    if f_key == t_key:
                        if f_value >= t_value:
                            msg = 'To Time must be greater than From Time.'
                            self._errors['to_time'] = self.error_class([msg])

