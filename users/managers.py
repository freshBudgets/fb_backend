# users/managers.py

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

################
# USER MANAGER #
################

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password, first_name="", last_name="", is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address")

        new_user = self.model( 
                email = email,
                phone = phone,
                first_name = first_name,
                last_name = last_name,
                is_staff = False,
                is_admin = False
            )
        new_user.set_password(password)
        new_user.save(using=self._db)

        return new_user

    def create_superuser(self, email, phone, password, is_staff=True, is_admin=True, first_name="", last_name=""):
        if not email:
            raise ValueError("User must have an email address")

        new_superuser = self.model( 
                email = email,
                phone = phone,
                first_name = first_name,
                last_name = last_name,
                is_staff = is_staff,
                is_admin = is_admin
            )
        new_superuser.set_password(password)
        new_superuser.save(using=self._db)

        return new_superuser

