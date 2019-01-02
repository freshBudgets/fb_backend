# budgets/admin.py

######################
# BUDGETS ADMIN PAGE #
######################

from .models import Budget
from django.contrib import admin

admin.site.register(Budget)
