from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
        HyperlinkedIdentityField,
        ModelSerializer,
        SerializerMethodField,
        ValidationError,
    )


User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone'
        ]

        # prevents returning json from displaying given password
        extra_kwargs = {'password': {'write_only': True}}
    
    # overrides ModelSerializer.create() to save the object in the database after creation
    def create(self, validated_data):
        email = validated_data['email'] 
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone = validated_data['phone']

        user_obj = User(
                email = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
            )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data
