__author__ = 'Cynthia'

from django import template
from tutors.models import *

register = template.Library()

@register.filter(name='recommend_course')
def recommend_course(user,course_id):
    if user and course_id:
        student = Student.objects.get(user=user)
        return Class.recommendation.through.objects.filter(student=student, class_id=course_id).exists()