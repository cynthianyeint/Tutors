# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0009_auto_20160401_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='student',
            field=models.ManyToManyField(to='tutors.Student', blank=True),
        ),
    ]
