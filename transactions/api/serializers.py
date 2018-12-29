# transactions/api/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


###########################
# TRANSACTION SERIALIZERS #
###########################

from transactions.models import Transaction

''' TransactionSerializerr
    - Serializes all data fed from TransactionViewSet
'''
class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'user_id',
            'budget_id',
            # 'account_id',
            'name',
            'amount',
            'date'
        ]

        extra_kwargs = {'user_id': {'read_only': True}}

    # TODO make sure we can't have duplicate transactions, just in case

    def create(self, validated_data):
        try:
            budget_id = validated_data['budget_id']
        except:
            budget_id = None
        # budget_id = validated_data['budget_id']
        name = validated_data['name']
        og_name = name
        amount = validated_data['amount']   
        date = validated_data['date']

        current_user = self.context['request'].user

        new_transaction = Transaction( 
                user_id = current_user.id,
                budget_id = budget_id,
                # account_id = account_id,
                name = name,
                amount = amount,
                date = date
            )  
        new_transaction.save()

        return new_transaction


