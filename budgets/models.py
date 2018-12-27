# budgets/models.py

from django.db import models

################
# BUDGET MODEL #
################

from django.contrib.auth import get_user_model
User = get_user_model()


class Budget(models.Model):
    user_id    = models.ForeignKey(User, on_delete=models.CASCADE)
    name       = models.CharField(max_length=255, blank=False)
    short_name = models.CharField(max_length=255, blank=True)
    limit      = models.FloatField()

    def __str__(self):
        return self.name
