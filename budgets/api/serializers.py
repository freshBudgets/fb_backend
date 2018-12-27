# budgets/api/serializers.py

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, EmailField

######################
# BUDGET SERIALIZERS #
######################

from budgets.models import Budget


class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'user_id',
            'name',
            'limit',
            'short_name',
        ]

    def validate(self, data):
        name = data['name']
        limit = data['limit']
        short_name = data['short_name']

        current_user = self.context['request'].user

        # prevent user from having two same named budgets
        query = Budget.objects.filter( 
                user_id = current_user.id,
                name = name
            )
        if query.exists():
            raise serializers.ValidationError("User already has a budget with given name")

        return data
