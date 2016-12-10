# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20161211_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='login',
            field=models.ForeignKey(to_field='username', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usefulnessrating',
            name='ratee',
            field=models.ForeignKey(related_name='ratee', to=settings.AUTH_USER_MODEL, to_field='username'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usefulnessrating',
            name='rater',
            field=models.ForeignKey(related_name='rater', to=settings.AUTH_USER_MODEL, to_field='username'),
            preserve_default=True,
        ),
    ]
