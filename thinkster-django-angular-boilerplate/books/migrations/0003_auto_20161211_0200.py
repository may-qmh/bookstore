# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20161210_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='username'),
            preserve_default=True,
        ),
    ]
