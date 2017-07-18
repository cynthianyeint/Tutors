from django.contrib import admin
from tutors.models import *


class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'teacher',]


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', ]


admin.site.register(ClassCategory)
admin.site.register(Class, ClassAdmin)
admin.site.register(Teacher, TeacherAdmin)
