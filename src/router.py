# src/router.py

from rest_framework import routers

# Router handles all default viewset urls
router = routers.DefaultRouter()

from budgets.api.views import BudgetViewSet
router.register('budgets', BudgetViewSet, basename='budgets')

from transactions.api.views import TransactionViewSet
router.register('transactions', TransactionViewSet, basename='transactions')
