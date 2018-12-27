# budgets/api/views.py

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
    )


######################
# BUDGET API VIEWSET #
######################

from budgets.models import Budget
from .serializers import BudgetSerializer

'''         Budget View Set

    GET     /api/budgets/       list budgets for current user
    POST    /api/budgets/       create budget for current user
    GET     /api/budgets/:id/   retrieve budget information
    PUT     /api/budgets/:id/   update budget information
    DELETE  /api/budgets/:id/   destroy budget
'''
class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Budget.objects.filter(user_id = current_user.id)





####################
# BUDGET API VIEWS #
####################

# # OUTDATED
# class BudgetAPIView(ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BudgetSerializer

#     def get_queryset(self):
#         current_user = self.request.user
#         return Budgets.objects.filter(user_id = current_ueser.id)

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = BudgetSerializer(data=data, context={'request': request})
#         current_user = request.user

#         # if data is not valid with serializer, raise exception
#         if serializer.is_valid(raise_exception=True):
#             serializer.save() 
#             return Response(serializer.data, HTTP_200_OK)

#         else:
#             return Response(HTTP_400_BAD_REQUEST)

# # OUTDATED
# class BudgetUpdateAPIView(UpdateAPIView):
#     permission_classea = [IsAuthenticated]
#     serializer_class = BudgetSerializer

#     def get_queryset(self):
#         current_user = self.request.user
#         return Budgets.objects.filter(user_id = current_user.id)
    
