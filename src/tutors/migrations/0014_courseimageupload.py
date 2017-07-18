# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tutors.models


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0013_teacher_youtube_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseImageUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('images', models.ImageField(upload_to=tutors.models.course_upload_to, null=True, verbose_name=b'Course Images', blank=True)),
                ('class_obj', models.ForeignKey(to='tutors.Class')),
            ],
        ),
    ]
