__author__ = 'lian'

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django import setup
from django.contrib.auth.models import User
from tutors.models import Teacher, Student

setup()


def get_random_name():
    from string import ascii_letters
    from random import sample

    return ''.join(sample(ascii_letters, 10))


def make_email(name):
    return name + '@testersunited.com.mm'


class UserTest(TestCase):
    def setUp(self):
        pass

    def test_activation_key(self):
        from tutors.user import create_activation_key
        key = create_activation_key("some_string")

        self.assertTrue(key is not None and len(key) > 10)

        key2 = create_activation_key("some_string")

        self.assertTrue(key2 is not None and len(key2) > 10)

        key3 = create_activation_key("some new string")

        self.assertTrue(key3 is not None and len(key3) > 10)

        self.assertNotEquals(key, key2)
        self.assertNotEquals(key2, key3)
        self.assertNotEquals(key, key3)

    def test_random_name(self):
        name = get_random_name()
        name2 = get_random_name()

        self.assertNotEquals(name, name2)

    def test_random_email(self):
        email = make_email('tester')
        self.assert_(email and email is not None and len(email) and '@' in email and '.' in email and 'tester' in email)

    def test_teacher_email_activation_view(self):
        # todo
        pass

    def test_teacher_register(self):
        client = Client()
        client_csrf = Client(enforce_csrf_checks=True)

        # get the registration page
        response = client.get(reverse('teacher-user-register'))
        self.assert_(response.status_code == 200)

        # prepare data to send
        random_name = 'tester_' + get_random_name()
        random_email = make_email(random_name)

        post_data = {
            'teacherform-title': 'mr.',
            'teacherform-first_name': random_name,
            'teacherform-dob_year': '2015',
            'teacherform-dob_month': '1',
            'teacherform-dob_day': '1',
            'userform-email': random_email,
            'userform-password1': 'test1234',
            'userform-password2': 'test1234',
        }

        # send a post (CSRF check)
        response = client_csrf.post(reverse('teacher-user-register'), data=post_data)
        self.assert_(response.status_code == 403, "There was no csrf error where it should be.")

        # send a post (register a teacher)
        response = client.post(reverse('teacher-user-register'), data=post_data)

        # should redirect to activation-sent page
        self.assert_(response.status_code == 302, "Not redirecting after teacher registration like it should.")
        self.assert_(reverse('activation-sent') in response.url, "Redirecting to wrong URL")

        # check teacher and user objects
        self.assert_(Teacher.objects.filter(first_name=random_name).exists(), "Teacher was not created via teacher register form.")
        self.assert_(User.objects.filter(email=random_email).exists(), "User was not created via teacher register form.")

        teacher = Teacher.objects.filter(first_name=random_name).first()

        self.assertIsNotNone(teacher)
        self.assertIsNotNone(teacher.user)

        user = teacher.user

        # check user email
        self.assert_(user.email == random_email, "User's email was not set properly.")
        self.assert_(teacher.email == random_email, "Teacher's email was not set properly.")

        # check "user_activated" property
        self.assertFalse(teacher.user_activated, "Teach was erroneously activated on register.")

        # check form for user requesting new activation code
        resend_url = reverse('resend-activation', kwargs={'user_id': user.id})
        response = client.get(resend_url)
        self.assert_(response.status_code == 200)
        self.assert_('csrfmiddlewaretoken' in response.content)
        self.assert_('id="form-resend-activation"' in response.content)

        # check user's fullname, without last name
        self.assert_(teacher.fullname == "Mr. " + random_name)

    def test_student_register(self):
        client = Client()
        client_csrf = Client(enforce_csrf_checks=True)

        #get student registration page
        response = client.get(reverse('student-register'))
        self.assert_(response.status_code == 200)

        random_name = "tester_student_" + get_random_name()
        random_email = make_email(random_name)

        #data to send
        post_data = {
            'studentform-title': 'ms.',
            'studentform-first_name': random_name,
            'studentform-dob_year': '1993',
            'studentform-dob_month': '4',
            'studentform-dob_day': '1',
            'userform-email': random_email,
            'userform-password1': '123',
            'userform-password2': '123',
        }

        #send a post (CSRF check)
        response = client_csrf.post(reverse('student-register'), data=post_data)
        self.assert_(response.status_code == 403, "There was no csrd error where it should be.")

        #send a post(register student)
        response = client.post(reverse('student-register'), data=post_data)

        #should redirect to activation page
        self.assert_(response.status_code == 302, "Not redirecting after student registration like it should.")
        self.assert_(reverse('activation-sent') in response.url, "Redirecting to wrong URL.")

        #check student & user objects
        self.assert_(Student.objects.filter(first_name=random_name).exists(), "Student was not created by student registration form.")
        self.assert_(User.objects.filter(email=random_email).exists(), "User was not created by student registration form.")

        student = Student.objects.filter(first_name=random_name).first()
        user = student.user

        self.assertIsNotNone(student)
        self.assertIsNotNone(user)

        #check user email
        self.assert_(user.email == random_email, "User's email was not set properly.")
        self.assert_(student.email == random_email, "Student's email was not set properly")

        #check "user_activated" property
        self.assertFalse(student.user_activated, "Student was erroneously activated on register.")

        #check form for user requesting new activation code
        resend_url = reverse('resend-activation', kwargs={'user_id': user.id})
        response = client.get(resend_url)
        self.assert_(response.status_code == 200)
        self.assert_('csrfmiddlewaretoken' in response.content)
        self.assert_('id="form-resend-activation"' in response.content)
