# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20161211_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn10',
            field=models.CharField(max_length=10, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')]),
            preserve_default=True,
        ),
    ]
