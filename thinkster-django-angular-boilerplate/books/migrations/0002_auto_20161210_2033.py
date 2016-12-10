# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='login',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column='username'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='login',
            field=models.ForeignKey(db_column='username', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
