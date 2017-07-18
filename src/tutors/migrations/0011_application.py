# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0010_class_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=100, null=True, blank=True)),
                ('course', models.ForeignKey(to='tutors.Class')),
                ('student', models.ForeignKey(to='tutors.Student')),
                ('teacher', models.ForeignKey(to='tutors.Teacher')),
            ],
        ),
    ]
