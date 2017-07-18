from django.contrib.auth.models import User
from notifications.models import Notification
from notifications.signals import notify

__author__ = 'Cynthia'

from django import setup

setup()

from unittest import TestCase
from tutors.models import Student, Teacher, Class, ClassCategory, Application


class NotificationTest(TestCase):
    def setUp(self):
        self.todelete= []

        self.teacher_user = User(username='testteacher@gmail.com', email='testteacher@gmail.com', password='testteacher123')
        self.teacher_user.save()
        self.todelete.append(self.teacher_user)

        self.student_user = User(username='teststudent@gmail.com', email='teststudent@gmail.com', password='teststudent123')
        self.student_user.save()
        self.todelete.append(self.student_user)

        self.teacher = Teacher(title="mr.", first_name="testTeacher", dob="1960-07-03", user=self.teacher_user)
        self.teacher.save()
        self.todelete.append(self.teacher)

        self.student = Student(title="mr.", first_name="testStudent", dob="1992-01-02", user=self.student_user)
        self.student.save()
        self.todelete.append(self.student)

        self.category = ClassCategory(name="TestCourse")
        self.category.save()
        self.todelete.append(self.category)

        self.course = Class(title="TestCourse", teacher=self.teacher, category=self.category)
        self.course.save()
        self.todelete.append(self.course)

    def test_application_noti(self):

        self.assertIsNotNone(self.teacher, "No existing teacher was found.")
        self.assertIsNotNone(self.student, "No existing student was found.")
        self.assertIsNotNone(self.course, "No existing course was found.")

        self.application = Application()
        self.assertNotEqual(self.application.course_id, self.course.id, "Course application ald existed.")

        #add application data
        self.application = Application(status="PendingTest", student=self.student, teacher=self.teacher, course=self.course)
        self.application.save()
        self.assertEqual(self.application.course_id, self.course.id, "No course application found.")

        #test notifications(send notification to teacher)
        self.assert_(self.application.pending_app_noti is False)
        notify.send(self.student, recipient=self.application.teacher.user, verb="applied", target=self.application, description=self.course)
        self.assert_(self.application.pending_app_noti is True)

        #change application status to confirmed
        self.confirmed_application = Application.objects.get(pk=self.application.id)
        self.confirmed_application.status = "Confirmed"
        self.confirmed_application.save()

        #test notifications(send application approved noti to student)
        self.assert_(self.confirmed_application.confirm_app_noti is False)
        notify.send(self.teacher, recipient=self.confirmed_application.student.user, verb="approved admission to", target=self.confirmed_application, description=self.course)
        self.assert_(self.confirmed_application.confirm_app_noti is True)

        self.todelete.append(self.application)
        self.todelete.append(self.confirmed_application)

    def tearDown(self):
        Notification.objects.filter(target_object_id=self.application.id).delete()
        for c in self.todelete:
            c.delete()

