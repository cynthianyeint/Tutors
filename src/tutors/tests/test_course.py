__author__ = 'lian'

from django import setup

setup()

from unittest import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from tutors.models import Teacher, Class, ClassCategory, ClassSchedule, TimeSlot


class CourseTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.first()

        self.assert_(self.teacher is not None, "No existing teacher was found to test courses.")

        self.cat = ClassCategory(name="Cat")
        self.cat.save()

        self.cls = Class(title="Class", teacher=self.teacher, category=self.cat)
        self.cls.save()

    def test_course(self):
        self.assert_(self.cls is not None)

        schedule = ClassSchedule()
        schedule.cls = self.cls
        schedule.save()

        self.assert_(schedule is not None)

        # MONDAY - false
        self.assert_(self.cls.day_mon is False)

        TimeSlot(schedule=schedule, int_day=1, from_time="11:00:00", to_time="12:00:00").save()

        # MONDAY - true
        self.assert_(self.cls.day_mon is True)
        self.assert_(len(self.cls.get_class_schedule) == 1)

        # TUESDAY - false
        self.assert_(self.cls.day_tue is False)

        TimeSlot(schedule=schedule, int_day=2, from_time="11:00:00", to_time="12:00:00").save()

        # TUESDAY - true
        self.assert_(self.cls.day_tue is True)
        self.assert_(len(self.cls.get_class_schedule) == 2)

        # WED - false
        self.assert_(self.cls.day_wed is False)

        TimeSlot(schedule=schedule, int_day=3, from_time="11:00:00", to_time="12:00:00").save()

        # WED - true
        self.assert_(self.cls.day_wed is True)
        self.assert_(len(self.cls.get_class_schedule) == 3)

        # THUR - false
        self.assert_(self.cls.day_thu is False)

        TimeSlot(schedule=schedule, int_day=4, from_time="11:00:00", to_time="12:00:00").save()

        # THUR - true
        self.assert_(self.cls.day_thu is True)
        self.assert_(len(self.cls.get_class_schedule) == 4)

        # FRI - false
        self.assert_(self.cls.day_fri is False)

        TimeSlot(schedule=schedule, int_day=5, from_time="11:00:00", to_time="12:00:00").save()

        # FRI - true
        self.assert_(self.cls.day_fri is True)
        self.assert_(len(self.cls.get_class_schedule) == 5)

        # SAT - false
        self.assert_(self.cls.day_sat is False)

        TimeSlot(schedule=schedule, int_day=6, from_time="11:00:00", to_time="12:00:00").save()

        # SAT - true
        self.assert_(self.cls.day_sat is True)
        self.assert_(len(self.cls.get_class_schedule) == 6)

        # SUN - false
        self.assert_(self.cls.day_sun is False)

        TimeSlot(schedule=schedule, int_day=7, from_time="11:00:00", to_time="12:00:00").save()

        # SUN - true
        self.assert_(self.cls.day_sun is True)
        self.assert_(len(self.cls.get_class_schedule) == 7)

        # one more on sunday
        TimeSlot(schedule=schedule, int_day=7, from_time="13:00:00", to_time="14:30:00").save()
        self.assert_(len(self.cls.get_class_schedule) == 8)

        # one more on monday
        TimeSlot(schedule=schedule, int_day=1, from_time="13:00:00", to_time="14:30:00").save()
        self.assert_(len(self.cls.get_class_schedule) == 9)

        # one more on tuesday
        TimeSlot(schedule=schedule, int_day=2, from_time="13:00:00", to_time="14:30:00").save()
        self.assert_(len(self.cls.get_class_schedule) == 10)
