__author__ = 'Cynthia'

from django import template
from tutors.models import Teacher, Student

register = template.Library()


@register.filter(name='pending_app')
def pending_app(user):
    if user:
        if user.groups.filter(name='Teacher'):
            login_user = Teacher.objects.get(user=user)
        else:
            login_user = Student.objects.get(user=user)

        return login_user.get_pending_applications.exists()


@register.filter(name='pending_app_count')
def pending_app_count(user):
    if user:
        if user.groups.filter(name="Teacher"):
            teacher = Teacher.objects.get(user=user)
            total_pending_applications = teacher.get_pending_applications.count()
        else:
            student = Student.objects.get(user=user)
            total_pending_applications = student.get_pending_applications.count()

        return total_pending_applications