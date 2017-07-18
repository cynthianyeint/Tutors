from swingtime.models import EventType
from tutors.models import ClassCategory, Class, Teacher
from django.contrib.auth.models import User

__author__ = 'Cynthia'

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import Group, Permission

perms = {
    'Teacher':[
        'add_class',
        'edit_class',
        'delete_class',
    ],
    'Student':[
        'add_class', # todo: can student add class?
    ]
    }

class_category = ['Beginner', 'Intermediate', 'UpperIntemediate', 'Advance', 'IELTS', 'TOEFL']

classes = {
    'Beginner': [
        'Basic English',
        'English 1'
    ],
    'Intermediate': [
        'Intermediate English',
        'English II'
    ],
    'Upper Intermediate': [
        'English III'
    ],
    'Advanced': [
        'Advanced English',
        'English IV'
    ],
    'Exam Preparation': [
        'TOEFL', 'IELTS'
    ]
}

if User.objects.filter(first_name='GTO').count() == 0:
    user = User(username='gto', email='gto@gto.com', first_name='GTO', last_name='GTO').save()
else:
    user = User.objects.filter(first_name='GTO').first()

if Teacher.objects.filter(first_name='GTO').count() == 0:
    mock_teacher = Teacher(first_name='GTO', last_name='Onizuka', user=user).save()
else:
    mock_teacher = Teacher.objects.filter(first_name='GTO').first()


def setupperm():
    for group_name, perm_list in perms.iteritems():
        if Group.objects.filter(name=group_name).count() == 0:
            group = Group(name=group_name)
            group.save()

            for perm in perm_list:
                group.permissions.add(Permission.objects.filter(codename=perm).first())

            group.save()


# def setupclasscategory():
#     for c in class_category:
#         if ClassCategory.objects.filter(name=c).count() == 0:
#             ClassCategory(name=c).save()


def setupclasscategoryandclasses():
    for cat in classes:
        # add category
        if ClassCategory.objects.filter(name=cat).count() == 0:
            cat_obj = ClassCategory(name=cat).save()
        else:
            cat_obj = ClassCategory.objects.filter(name=cat).first()

        # add classes
        cl = classes[cat]
        for c in cl:
            if mock_teacher and cat_obj and Class.objects.filter(title=c).count() == 0:
                Class(title=c, category=cat_obj, teacher=mock_teacher).save()

def setupclassevent():
    if EventType.objects.filter(label='Fixed').count() == 0:
        event_type = EventType(abbr="fx", label="Fixed").save()

    if EventType.objects.filter(label='Weekly').count() == 0:
        event_type = EventType(abbr="wk", label="Weekly").save()



class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        setupperm()
        setupclasscategoryandclasses()
        setupclassevent()