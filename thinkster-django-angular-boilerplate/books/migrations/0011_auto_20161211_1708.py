# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_auto_20161211_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='order_date',
            field=models.DateField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
    ]
