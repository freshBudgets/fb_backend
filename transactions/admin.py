# budgets/admin.py

###########################
# TRANSACTIONS ADMIN PAGE #
###########################

from .models import Transaction
from django.contrib import admin

admin.site.register(Transaction)
