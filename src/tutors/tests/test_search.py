__author__ = 'nyantun'

from unittest import TestCase
from django import setup
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.test import Client
from tutors.models import Teacher, Class, ClassSchedule, ClassCategory, TimeSlot
from tutors.views import SearchList

setup()


class TestSearchListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'test123@gmail.com'
        self.email = 'test123@gmail.com'
        self.password = 'test-password'
        User.objects.filter(username=self.username).delete()
        self.test_user = User.objects.create_superuser(self.username, self.email, self.password)
        self.test_user.save()

        self.title = "mr."
        self.first_name = 'test_first_name'
        self.last_name = "test_last_name"
        self.nickname = "test_nick_name"
        self.dob = "1900-01-03"
        self.website = "http://www.google.com"
        self.user = self.test_user

        self.teacher = Teacher(title=self.title, first_name=self.first_name, last_name=self.last_name, nickname=self.nickname, dob=self.dob, website=self.website, user=self.user)
        self.teacher.save()

        self.login = self.client.login(username=self.username, password=self.password)

        self.class_category = ClassCategory.objects.all().first()

        self.class_title = "test_class_title"
        self.class_desc = "test_description"
        self.tutor_class = Class(title=self.class_title, category=self.class_category, teacher=self.teacher, description=self.class_desc)
        self.tutor_class.save()

        self.class_schedule = ClassSchedule(cls=self.tutor_class)
        self.class_schedule.save()

        self.schedule = self.class_schedule
        self.int_day = 1
        self.from_time = "09:00:00"
        self.to_time = "05:00:00"
        self.time_slot = TimeSlot(schedule=self.schedule, int_day=self.int_day, from_time=self.from_time, to_time=self.to_time)
        self.time_slot.save()

        self.view = SearchList()

    def test_search_nick_name(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_nick_name'] = 'test_nick_name'
        result = self.view.get_queryset()
        self.assertTrue(result.count() == 1)

    def test_search_first_name(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_first_name'] = 'test_first_name'
        result = self.view.get_queryset()
        self.assertTrue(result.count() == 1)

    def test_search_last_name(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_last_name'] = 'test_last_name'
        result = self.view.get_queryset()
        self.assertTrue(result.count() == 1)

    def test_search_website(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_website'] = "http://www.google.com"
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def test_search_dob(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_dob'] = "1900-01-03"
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def test_search_class_title(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_class_title'] = "test_class_title"
        result = self.view.get_queryset()
        self.assertTrue(result.count() == 1)

    def test_search_class_category_name(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_class_category_name'] = self.class_category.pk
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def test_search_description(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_description'] = "test_description"
        result = self.view.get_queryset()
        self.assertTrue(result.count() == 1)

    def test_search_int_day(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_int_day'] = 1
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def test_search_from_time(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_from_time'] = "09:00:00"
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def test_search_to_time(self):
        self.view.request = HttpRequest()
        self.view.request.GET['search_to_time'] = "05:00:00"
        result = self.view.get_queryset()
        self.assertTrue(result.count() > 0)

    def tearDown(self):
        # del self.test_user
        # del self.teacher
        # del self.tutor_class
        # del self.class_schedule
        # del self.time_slot
        User.objects.filter(username=self.username).delete()
        Teacher.objects.filter(pk=self.teacher.id).delete()
        Class.objects.filter(pk=self.tutor_class.id).delete()
        ClassSchedule.objects.filter(pk=self.class_schedule.id).delete()
        TimeSlot.objects.filter(pk=self.time_slot.id).delete()