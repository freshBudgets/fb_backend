# users/test_registration.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


""" User Registration tests
    ----------------------- 
    test_register
    test_bad_register
"""

@pytest.mark.django_db
class TestUserRegistration(TestCase):
    
    def setUp(self):
        self.client = APIClient()


    def test_register(self):
        register_url = reverse('register')

        # valid registration should respond OK
        valid_data = {
            'email': 'test@gmail.com',
            'phone': '1',
            'password': 'test_pass',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(register_url, valid_data, format='json')
        assert response.status_code == HTTP_200_OK
        assert 'user info' in response.data
        assert 'tokens' in response.data

        # register user with previously used email and phone
        valid_data = {
            'email': 'test@gmail.com',
            'phone': '1',
            'password': 'test_pass',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(register_url, valid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == "user with this email address already exists."
        assert response.data['phone'][0] == "user with this phone already exists."


    def test_bad_register(self):
        register_url = reverse('register')

        # register with no data
        invalid_data = {}
        response = self.client.post(register_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == "This field is required."
        assert response.data['password'][0] == "This field is required."
        assert response.data['phone'][0] == "This field is required."

        # register with blank data
        invalid_data = {
            'email': '',
            'phone': '',
            'password': ''
        }
        response = self.client.post(register_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == "This field may not be blank."
        assert response.data['password'][0] == "This field may not be blank."
        assert response.data['phone'][0] == "This field may not be blank."

        # register with invalid email address
        invalid_data = {
            'email': 'invalid_email_address',
            'phone': '',
            'password': '',
            'first_name': '',
            'last_name': ''
        }
        response = self.client.post(register_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['email'][0] == "Enter a valid email address."

