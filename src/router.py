from rest_framework import routers
from budgets.api.views import (
        BudgetViewSet,
    ) 

router = routers.DefaultRouter()

router.register('budgets', BudgetViewSet, basename='budgets')
