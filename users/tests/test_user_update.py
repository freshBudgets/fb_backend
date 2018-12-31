# users/test_user_update.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


""" User Update tests
    ----------------------- 
"""

@pytest.mark.django_db
class TestUserUpdate(TestCase):
    pass
