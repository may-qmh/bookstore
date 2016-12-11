# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_auto_20161212_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usefulnessrating',
            name='isbn10',
            field=models.ForeignKey(to='books.Book', db_column='isbn10'),
            preserve_default=True,
        ),
    ]
