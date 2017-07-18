# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0016_auto_20160524_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='youtube_link',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(regex=b'^(?:https?:\\/\\/)?(?:m\\.|www\\.)?(?:youtu\\.be\\/|youtube\\.com\\/(?:embed\\/|v\\/|watch\\?v=|watch\\?.+&v=))((\\w|-){11})(?:\\S+)?$', message=b'Please enter valid youtube link.')]),
        ),
    ]
