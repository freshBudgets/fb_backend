# accounts.models

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from .managers import UserManager

class User(AbstractBaseUser):
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name  = models.CharField(max_length=255, blank=True)
    last_name   = models.CharField(max_length=255, blank=True)
    phone       = models.CharField(max_length=20, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True) # can login
    is_staff    = models.BooleanField(default=False) # is staff
    is_admin    = models.BooleanField(default=False) # is superuser/admin

    # changes 'username' field to be 'email' so users login with email instead of username
    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = ['phone']
    # assign UserManager as a manager for User
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


