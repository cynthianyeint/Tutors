# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0014_courseimageupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='recommendation',
            field=models.ManyToManyField(related_name='recommendation', to='tutors.Student', blank=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='student',
            field=models.ManyToManyField(related_name='student', to='tutors.Student', blank=True),
        ),
    ]
