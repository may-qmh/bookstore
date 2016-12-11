# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20161211_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.FloatField(default=0.0, blank=True),
            preserve_default=True,
        ),
    ]
