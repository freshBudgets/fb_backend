# accounts.managers

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)



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



# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("User must have an email address")

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     def create_user(self, email, first_name, last_name, phone, is_active=True, is_staff=False, is_admin=False, password=None):
#         if not email:
#             raise ValueError("User must have an email address")
#         if not phone:
#             raise ValueError("User must have a phone number")

#         user = self.model( 
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             phone = phone,
#         )
#         user.is_staff = is_staff
#         user.is_admin = is_admin
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

        

#     def create_superuser(self, email, phone, first_name, last_name, password):
#         if not email:
#             raise ValueError("User must have an email address")
#         if not phone:
#             raise ValueError("User must have a phone number")

#         user = self.model( 
#             email = self.normalize_email(email),
#             password = password,
#             first_name = first_name,
#             last_name = last_name,
#             phone = phone,
#             is_staff = True,
#             is_admin = True
#         )

#         user.save(using=self._db)
#         return user

