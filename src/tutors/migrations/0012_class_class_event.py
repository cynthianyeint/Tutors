# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swingtime', '0001_initial'),
        ('tutors', '0011_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_event',
            field=models.OneToOneField(null=True, default=b'', blank=True, to='swingtime.Event'),
        ),
    ]
