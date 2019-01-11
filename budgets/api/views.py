# budgets/api/views.py

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

######################
# BUDGET API VIEWSET #
######################

from budgets.models import Budget
from .serializers import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all budgets for current user

    create:
    Create a new budget instance for current user

    retrieve:
    Retrieve budget information for single budget instance along with transactions in existing budget

    update:
    Update budget information

    destroy:
    Delete budget instance
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    # define all objects to be queried
    # In this case, only query budgets for current user
    def get_queryset(self):
        current_user = self.request.user
        return Budget.objects.filter(user_id = current_user.id)

    
    def retrieve(self, request, pk=None):
        budget = Budget.objects.get(id=pk)
        budget_info = {}

        budget_info['name'] = budget.name
        budget_info['limit'] = budget.limit

        # TODO return transactions, paginated

        return Response(budget_info, HTTP_200_OK)
