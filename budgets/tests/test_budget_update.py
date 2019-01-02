# budgets/test_budget_update.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from budgets.api.views import BudgetViewSet

@pytest.mark.django_db
class TestBudgetUpdate(TestCase):
    """ Budget Update test
        -------------------- 
        test_budget_update
        test_bad_budget_update
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


    def test_budget_update(self):
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

        # update the newly created budget
        budget_id = response.data['id']

        budget_update_data = {
            'id': budget_id,
            'name': 'new name',
            'limit': 300
        }

        budget_update_url = view.reverse_action('detail', args=(budget_id,))
        response = self.client.put(budget_update_url, budget_update_data, format='json')
        
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == budget_id
        assert response.data['name'] == 'new name'
        assert response.data['limit'] == 300


    def test_bad_budget_update(self):
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

        budget_id = response.data['id']
        
        # blank data
        invalid_data = {}

        budget_update_url = view.reverse_action('detail', args=(budget_id,))
        response = self.client.put(budget_update_url, invalid_data, format='json')
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['name'][0] == "This field is required."
        assert response.data['limit'][0] == "This field is required."


        # invalid data
        invalid_data = {
            'name': '',
            'limit': ''
        }

        response = self.client.put(budget_update_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['name'][0] == "This field may not be blank."
        assert response.data['limit'][0] == "A valid number is required."
