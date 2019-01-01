# budgets/models.py

from django.db import models


################
# BUDGET MODEL #
################

from django.contrib.auth import get_user_model
User = get_user_model()

''' Budget Model
    - Is linked to user instance through user_id
    - Stores information on a budget
'''
class Budget(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255, blank=False)
    limit   = models.FloatField()

    def __str__(self):
        return self.name
