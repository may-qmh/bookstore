from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import Account
from django.core.validators import RegexValidator, MinValueValidator
class Book(models.Model):
    isbn10 = models.CharField(validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')],primary_key=True, max_length=10)
    title = models.CharField(max_length=256)
    authors = models.CharField(max_length=256, blank=True, null=True)
    publisher = models.CharField(max_length=64, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField()
    price = models.FloatField(validators = [MinValueValidator(0.0)],blank=True,default=0.0)
    formatchoices = (
        ('hardcover', 'hardcover'),
        ('paperback', 'paperback')
    )
    format = models.CharField(max_length=9, blank=True, null=True, choices=formatchoices)
    keyword = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=256,blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'book'


class BookOrdered(models.Model):
    oid = models.ForeignKey('OrderHistory', db_column='oid')
    isbn10 = models.ForeignKey('Book', db_column='isbn10')
    quantity = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'book_ordered'
        unique_together = (('oid', 'isbn10'),)




# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'django_migrations'
#         app_label = 'mainpage'

class Feedback(models.Model):
    entry_date = models.DateField(auto_now_add=True, null=True)
    scorechoices = zip(range(0,11), range(0,11))
    score = models.IntegerField(choices=scorechoices)
    opinion = models.CharField(max_length=256, blank=True, null=True)
    login = models.ForeignKey(Account,to_field='username')
    isbn10 = models.ForeignKey('Book', db_column='isbn10')

    class Meta:
        managed = True
        db_table = 'feedback'
        unique_together = (('login', 'isbn10'),)


class OrderHistory(models.Model):
    oid = models.AutoField(primary_key=True)
    login = models.ForeignKey(Account,to_field='username', blank=True, null=True)
    order_date = models.DateField(auto_now_add=True,blank=True, null=True)
    statuschoices = (
        ('processing', 'processing order'),
        ('transit', 'in transit'),
        ('delivered', 'delivered')
    )
    order_status = models.CharField(max_length=16, blank=True, null=True, choices=statuschoices)

    class Meta:
        managed = True
        db_table = 'order_history'

class UsefulnessRating(models.Model):
    def clean(self):
        if (self.rater_id == self.ratee_id):
            raise ValidationError('rater_id == ratee _id')

    rater = models.ForeignKey(Account,to_field='username', related_name='rater')
    ratee = models.ForeignKey(Account,to_field='username', related_name='ratee')
    usefulnesschoices = (
        (0,0),
        (1,1),
        (2,2)
    )
    usefulness = models.IntegerField(choices=usefulnesschoices)
    isbn10 = models.ForeignKey(Book, db_column='isbn10')

    class Meta:
        managed = True
        db_table = 'usefulness_rating'
        unique_together = (('rater', 'ratee', 'isbn10'),)