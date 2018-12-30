# users/test_login.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from users.api.views import UserCreateAPIView, UserLoginAPIView

""" Login and Auth tests
    -------------------- 
    test_login
    test_bad_login
    test_auth
"""

@pytest.mark.django_db
class TestUserLoginAndAuth(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        # register users for use in login tests
        register_url = reverse('register')
        user_1 = {
            'email': 'test@gmail.com',
            'phone': '1',
            'password': 'test_pass',
            'first_name': 'first',
            'last_name': 'last'
        }
        response = self.client.post(register_url, user_1, format='json')


    def test_login(self):
        login_url = reverse('login')

        # login user with only email
        valid_data = {
            'email': 'test@gmail.com',
            'phone': '',
            'password': 'test_pass'
        }
        response = self.client.post(login_url, valid_data, format='json')
        assert response.status_code == HTTP_200_OK
        assert 'user info' in response.data
        assert 'tokens' in response.data
        
        # login user with only phone number
        valid_data = {
            'email': '',
            'phone': '1',
            'password': 'test_pass'
        }
        response = self.client.post(login_url, valid_data, format='json')
        assert response.status_code == HTTP_200_OK
        assert 'user info' in response.data
        assert 'tokens' in response.data

    def test_bad_login(self):
        login_url = reverse('login')

        # blank data
        invalid_data = {}
        response = self.client.post(login_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['password'][0] == "This field is required."

        # invalid credentials
        invalid_data = { 
            'email': 'not_a_registered_email@gmail.com',
            'phone': '0',
            'password': 'password'
        }
        response = self.client.post(login_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    
    def test_auth(self):
        login_url = reverse('login')
        budgets_url = reverse('budgets-list')

        # login and obtain tokens
        valid_data = {
            'email': 'test@gmail.com',
            'phone':'1',
            'password': 'test_pass'
        }
        response = self.client.post(login_url, valid_data, format='json')
        access_token = response.data['tokens']['access token']
        refresh_token = response.data['tokens']['refresh token']

        # attempt to access protected bugdets view without JWT
        response = self.client.get(budgets_url)
        assert response.status_code == HTTP_401_UNAUTHORIZED

        # apply tokens and access same protected view
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(budgets_url)
        assert response.status_code == HTTP_200_OK


