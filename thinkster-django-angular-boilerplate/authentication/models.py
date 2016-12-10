from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, username=None, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a valid username.')


        account = self.model(
            username=username
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self,username,  password, **kwargs):
        account = self.create_user(username, password, **kwargs)

        account.is_admin = True
        account.save()

        return account
        
class Account(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)

    full_name = models.CharField(max_length=64, blank=True, null=True)
    credit_card = models.CharField(max_length=16, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username
