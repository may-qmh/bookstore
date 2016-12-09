# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn10', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('authors', models.CharField(max_length=256, null=True, blank=True)),
                ('publisher', models.CharField(max_length=64, null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('stock', models.IntegerField()),
                ('price', models.FloatField(null=True, blank=True)),
                ('format', models.CharField(blank=True, max_length=9, null=True, choices=[('hardcover', 'hardcover'), ('paperback', 'paperback')])),
                ('keyword', models.CharField(max_length=100, null=True, blank=True)),
                ('subject', models.CharField(max_length=100, null=True, blank=True)),
                ('image', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'db_table': 'book',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookOrdered',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('isbn10', models.ForeignKey(to='books.Book', db_column='isbn10')),
            ],
            options={
                'db_table': 'book_ordered',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('login_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('full_name', models.CharField(max_length=64, null=True, blank=True)),
                ('password', models.CharField(max_length=16, null=True, blank=True)),
                ('credit_card', models.CharField(max_length=16, null=True, blank=True)),
                ('address', models.CharField(max_length=256, null=True, blank=True)),
                ('phone', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'customer',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_date', models.DateField(auto_now_add=True, null=True)),
                ('score', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('opinion', models.CharField(max_length=256, null=True, blank=True)),
                ('isbn10', models.ForeignKey(to='books.Book', db_column='isbn10')),
                ('login', models.ForeignKey(to='books.Customer')),
            ],
            options={
                'db_table': 'feedback',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('oid', models.IntegerField(serialize=False, primary_key=True)),
                ('order_date', models.DateField(null=True, blank=True)),
                ('order_status', models.CharField(blank=True, max_length=16, null=True, choices=[('processing', 'processing order'), ('transit', 'in transit'), ('delivered', 'delivered')])),
                ('login', models.ForeignKey(blank=True, to='books.Customer', null=True)),
            ],
            options={
                'db_table': 'order_history',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsefulnessRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usefulness', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2)])),
                ('isbn10', models.ForeignKey(to='books.Feedback', db_column='isbn10')),
                ('ratee', models.ForeignKey(related_name='ratee', to='books.Customer')),
                ('rater', models.ForeignKey(related_name='rater', to='books.Customer')),
            ],
            options={
                'db_table': 'usefulness_rating',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usefulnessrating',
            unique_together=set([('rater', 'ratee', 'isbn10')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([('login', 'isbn10')]),
        ),
        migrations.AddField(
            model_name='bookordered',
            name='oid',
            field=models.ForeignKey(to='books.OrderHistory', db_column='oid'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bookordered',
            unique_together=set([('oid', 'isbn10')]),
        ),
    ]
