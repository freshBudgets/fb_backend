# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

        
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, first name, 
        last name, phone, and password.
        """
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, first name,
        last name, phone, and password
        """
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name  = models.CharField(max_length=255, blank=True)
    last_name   = models.CharField(max_length=255, blank=True)
    phone       = models.CharField(max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True) # can login
    is_staff    = models.BooleanField(default=False) # is staff
    is_admin    = models.BooleanField(default=False) # is superuser/admin

    # changes 'username' field to be 'email' so users login with email instead of username
    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = []
    # assign UserManager as a manager for User
    objects = UserManager()

    def __str__(self):
        return self.email

    def __itr__(self):
        return [
            self.email,
            self.first_name,
            self.last_name,
            self.phone,
            self.date_joined,
            self.is_active,
            self.is_staff,
            self.is_admin
        ]

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

    # @property
    # def is_active(self):
    #     "Is this user active?"
    #     return self.is_active

    # @property
    # def is_admin(self):
    #     "Is this user a superuser?"
    #     return self.is_admin
