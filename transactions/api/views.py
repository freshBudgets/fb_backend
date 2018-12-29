# transactions/api/views.py

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
    )


###########################
# TRANSACTION API VIEWSET #
###########################

from transactions.models import Transaction
from .serializers import TransactionSerializer

'''         Transaction View Set

    GET     /api/transaction/       list transactions for current user
    POST    /api/transaction/       create transaction for current user
    GET     /api/transaction/:id/   retrieve transaction information
    PUT     /api/transaction/:id/   update transaction information
    DELETE  /api/transaction/:id/   destroy transaction
'''
class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        current_user = self.request.user
        return Transaction.objects.filter(user_id = current_user.id)


