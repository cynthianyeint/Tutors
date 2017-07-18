from django.db.models import Q

__author__ = 'Cynthia'


def in_teacher_group(user):
    return user.groups.filter(name='Teacher').exists()


def in_student_group(user):
    return user.groups.filter(name='Student').exists()


def group_check(user):
    return user.groups.filter(Q(name='Teacher') | Q(name='Student')).exists()