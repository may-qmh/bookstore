# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20161211_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='oid',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
