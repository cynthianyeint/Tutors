# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0015_auto_20160523_1551'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='youtube_link',
        ),
        migrations.AddField(
            model_name='class',
            name='youtube_link',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(regex=b'^(http|https)\\:\\/\\/www\\.youtube\\.com\\/watch\\?v\\=(\\w*)(\\&(.*))?$', message=b'Please enter valid youtube link.')]),
        ),
    ]
