# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0002_auto_20160315_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='title',
            field=models.CharField(max_length=20, null=True, choices=[(b'mr.', b'Mr.'), (b'ms.', b'Ms.'), (b'miss', b'Miss'), (b'mrs.', b'Mrs.')]),
        ),
    ]
