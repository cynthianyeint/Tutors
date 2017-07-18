# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='day',
            new_name='int_day',
        ),
    ]
