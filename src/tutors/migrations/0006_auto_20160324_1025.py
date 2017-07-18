# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0005_useractivation'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='enabled',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='class',
            name='published',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='title',
            field=models.CharField(max_length=20, null=True, choices=[(b'mr.', b'Mr.'), (b'ms.', b'Ms.')]),
        ),
    ]
