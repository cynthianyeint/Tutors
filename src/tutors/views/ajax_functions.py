from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from notifications.signals import notify
from tutors.models import Class, Student, Application, Teacher, UserProfile
import json

__author__ = 'Cynthia'


def get_class_data(request):
    data = ''
    if request.is_ajax():
        class_data = Class.objects.all()
        class_data_list = []
        for c in class_data:
            try:
                get_avatar = c.teacher.avatar_url                
            except Exception, ex:
                get_avatar = "/static/img/user_profile.jpg"
            teacher_name = c.teacher.get_teacher_name_with_tile
            get_category = c.category.name
            my_list = {'label': c.title, 'value': c.title, 'id': c.id, 'img': get_avatar, 'teacher': teacher_name, 'category': get_category}
            class_data_list.append(my_list)
            data = json.dumps(class_data_list)
    else:
        data = "fail"
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def course_apply_check(request):
    data = {}
    if request.GET and request.is_ajax():
        user_id = request.GET.get('user_id', '')
        course_id = request.GET.get('course_id', '')
        if user_id and course_id:
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            course = Class.objects.get(pk=course_id)

            if Class.objects.filter(pk=course_id, student__user=user).exists(): #check if student ald exists in course
                data['message'] = "existing_student"
            else:
                if not Application.objects.filter(course=course, student=student).exists(): #check if student ald submitted application
                    #add data into application
                    application = Application()
                    application.status = "Pending"
                    application.student = student
                    application.course = course
                    application.teacher = course.teacher
                    application.save()

                    #send notification to teacher
                    # notify.send(student, recipient=course.teacher.user, verb="applied", target=application, description=course)

                    data['message'] = "success"
                else:
                    data['message'] = "success"
        else:
            data['message'] = "fail"

    mimetype = 'application/json'

    return HttpResponse(json.dumps(data), mimetype)


def application_process(request):
    data = ''
    if request.GET and request.is_ajax():
        application_id = request.GET.get('application_id', '')
        application_status = request.GET.get('status', '')
        if application_id:
            application = Application.objects.filter(pk=application_id).first()

            if application_status == "confirm":

                #change application status to confirm
                application.status = "Confirmed"
                application.save()

                #add student into course
                application.course.student.add(application.student)

                #send notification to student
                # notify.send(application.teacher, recipient=application.student.user, verb="approved admission to", target=application, description=application.course)

            elif application_status == "reject":

                #change application status to rejected
                application.status = "Rejected"
                application.save()

                #send notification to student
                # notify.send(application.teacher, recipient=application.student.user, verb="rejected admission to", target=application, description=application.course)

            else:

                #change application status to cancelled
                application.status = "Cancelled"
                application.save()


            #mark notification as read
            # notification = get_object_or_404(Notification, recipient=application.teacher.user, target_object_id=application_id)
            # notification.mark_as_read()


            data = json.dumps(application_id)
        else:
            data = "fail"

        mimetype = 'application/json'

        return HttpResponse(data, mimetype)


def withdraw_course(request):
    data = ''
    if request.GET and request.is_ajax():
        course_id = request.GET.get('course_id','')
        student_user_id = request.user.id
        if course_id:
            student = Student.objects.get(user__id=student_user_id)
            course = Class.objects.get(pk=course_id)

            #remove student from course
            Class.student.through.objects.filter(class_id=course_id, student=student).delete()

            data = {'course_id': course_id, 'user_id': student_user_id, 'student_id': student.id}
            data = json.dumps(data)
    else:
        data = "fail"

    mimetype = 'appliation/json'
    return HttpResponse(data, mimetype)


def recommend_course(request):
    data = ''
    if request.GET and request.is_ajax():
        course_id = request.GET.get('course_id', '')
        student_id = request.GET.get('student_id', '')
        status = request.GET.get('status', '')

        if course_id and status:
            course = Class.objects.filter(pk=course_id).first()
            student = Student.objects.filter(pk=student_id).first()
            if status == 'like':
                course.recommendation.add(student)
            else:
                course.recommendation.remove(student)
            data = {'message': "success", 'count': course.recommendation.count()}
        else:
             data = {'message': "fail"}

    mimetype = 'applicatin/json'

    return HttpResponse(json.dumps(data), mimetype)
