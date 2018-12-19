# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, phone):
        """
        Creates and saves a User with the given email, first name, 
        last name, phone, and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, phone):
        """
        Creates and saves a superuser with the given email, first name,
        last name, phone, and password
        """
        user = self.create_user(
            email,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone = phone
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    phone       = models.CharField(max_length=20)
    timestamp   = models.DateTimeField(auto_now_add=True)
    is_active   = models.BooleanField(default=True) # can login
    is_staff    = models.BooleanField(default=False) # is staff
    is_admin    = models.BooleanField(default=False) # is superuser/admin

    # changes 'username' field to be 'email' so users login with email instead of username
    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    # assign UserManager as a manager for User
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

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
