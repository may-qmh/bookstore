# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20161211_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.FloatField(default=0.0, blank=True, validators=[django.core.validators.MinValueValidator(0.0)]),
            preserve_default=True,
        ),
    ]
