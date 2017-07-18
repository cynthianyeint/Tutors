# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0003_auto_20160316_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='title',
            field=models.CharField(max_length=20, null=True, choices=[(b'mr.', b'Mr.'), (b'ms.', b'Ms.'), (b'mrs.', b'Mrs.'), (b'dr.', b'Dr.'), (b'prof.', b'Prof.')]),
        ),
    ]
