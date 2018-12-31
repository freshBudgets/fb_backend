# budgets/test_budget_list.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


""" Budget Tests
    -------------------- 
"""

@pytest.mark.django_db
class TestBudgetListView(TestCase):
    
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
        access_token = response.data['tokens']['access token']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_budget_list(self):
        budget_list_url = reverse('budget-list') 
        response = self.client.get(budget_list_url)
        assert response.status_code == HTTP_200_OK

    def test_budget_create(self):
        budget_create_url = reverse('budget-create')
        
        data = {
            'name':
        }
