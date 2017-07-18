# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0017_auto_20160525_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='biography',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
