# budgets/test_budget_read.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from budgets.api.views import BudgetViewSet

@pytest.mark.django_db
class TestBudgetRead(TestCase):
    """ Budget Read test
        -------------------- 
        test_budget_read
    """
    
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


    def test_budget_read(self):
        # create a budget
        view = BudgetViewSet()
        view.basename = 'budgets'
        view.request = None
        budget_create_url = view.reverse_action('list')

        budget_create_data = {
            'name': 'budget',
            'limit': 100
        }
        response = self.client.post(budget_create_url, budget_create_data, format='json')

        # retrieve the budget info for the created budget
        budget_id = response.data['id']
        budget_detail_url = view.reverse_action('detail', args=(budget_id,))
        response = self.client.get(budget_detail_url) 

        assert response.data['name'] == 'budget'
        assert response.data['limit'] == 100





