# budgets/test_budget_create.py

import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from budgets.api.views import BudgetViewSet

@pytest.mark.django_db
class TestBudgetCreate(TestCase):
    """ Budget Create test
        -------------------- 
        test_budget_create
        test_bad_budget_create
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

    def test_budget_create(self):
        # this is how to obtain the url of an action from a viewset
        view = BudgetViewSet()
        view.basename = 'budgets'
        view.request = None
        # the 'create' action is just a POST on the 'list' url
        budget_create_url = view.reverse_action('list')

        valid_data = {
            'name': 'new budget',
            'limit': 20.50
        }

        response = self.client.post(budget_create_url, valid_data, format='json')
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'new budget'
        assert response.data['limit'] == 20.50

    
    def test_bad_budget_create(self):
        # this is how to obtain the url of an action from a viewset
        view = BudgetViewSet()
        view.basename = 'budgets'
        view.request = None
        # the 'create' action is just a POST on the 'list' url
        budget_create_url = view.reverse_action('list')
        

        # blank data
        invalid_data = {}
        response = self.client.post(budget_create_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['name'][0] == "This field is required."
        assert response.data['limit'][0] == "This field is required."


        # invalid data
        invalid_data = {
            'name': '',
            'limit': '',
        }
        response = self.client.post(budget_create_url, invalid_data, format='json')
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data['name'][0] == "This field may not be blank."
        assert response.data['limit'][0] == "A valid number is required."
