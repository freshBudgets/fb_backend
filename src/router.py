from rest_framework import routers
from budgets.api.views import BudgetViewSet
from transactions.api.views import TransactionViewSet

router = routers.DefaultRouter()

router.register('budgets', BudgetViewSet, basename='budgets')
router.register('transactions', TransactionViewSet, basename='transactions')
