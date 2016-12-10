# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20161211_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usefulnessrating',
            name='ratee',
            field=models.ForeignKey(related_name='ratee', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usefulnessrating',
            name='rater',
            field=models.ForeignKey(related_name='rater', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
