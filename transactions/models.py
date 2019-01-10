# /transactions/models.py

from django.db import models

#####################
# TRANSACTION MODEL #
#####################

from budgets.models import Budget
# from accounts.models import Account
from django.contrib.auth import get_user_model
User = get_user_model()

''' Transaction Model
    - Is linked to user instance through user_id
    - Is linked to budget instance through budget_id
    - If linked budget is deleted, budget_id is set to NULL
    - Is linked to account instance through account_id
    - If linked account is deleted, transaction will be deleted
    - Stores information on a transaction
'''
class Transaction(models.Model):
    user_id      = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_id    = models.ForeignKey(Budget, null=True, default=None, on_delete=models.SET_NULL)
    # account_id = models.ForeignKey(Account, null=False, on_delete=models.CASCADE)
    name         = models.CharField(max_length=255, blank=False)
    og_name      = models.CharField(max_length=255, blank=False) 
    amount       = models.FloatField()
    date         = models.DateField()

    def __str__(self):
        return self.name
