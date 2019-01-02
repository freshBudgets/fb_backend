# budgets/api/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


######################
# BUDGET SERIALIZERS #
######################

from budgets.models import Budget

""" BudgetSerializer
    - Serializes all data fed from BudgetViewSet
    - Prevents user from creating two budgets with the same name
"""
class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = [
            'id',
            'name',
            'limit',
        ]

    def validate(self, data):
        name = data['name']
        limit = data['limit']
        current_user = self.context['request'].user

        # prevent user from having two same named budgets
        query = Budget.objects.filter( 
                user = current_user,
                name = name
            )
        if query.exists():
            raise serializers.ValidationError("User already has a budget with given name")

        return data

    def create(self, validated_data):
        name = validated_data['name'] 
        limit = validated_data['limit']
        user = self.context['request'].user

        # create the new budget instance
        new_budget = Budget( 
                name = name,
                limit = limit,
                user = user
            )
        new_budget.save()

        return new_budget
