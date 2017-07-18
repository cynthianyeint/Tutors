# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tutors', '0008_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='home_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{6,15}$', message=b"Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='student',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{6,15}$', message=b"Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='teacher',
            name='home_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{6,15}$', message=b"Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")]),
        ),
        migrations.AddField(
            model_name='teacher',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{6,15}$', message=b"Phone number must be entered in the format: '+999999'. Up to 15 digits allowed.")]),
        ),
    ]
