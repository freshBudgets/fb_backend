# accounts/api/serializers.py

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
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


class UserLoginSerializer(serializers.ModelSerializer):
    email = EmailField(label='Email Address', allow_blank=True, required=False)
    phone = CharField(allow_blank=True, required=False)
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'phone',
            'password',
            'token',
        ]

        # prevents returning json from displaying given password
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data['email']
        phone = data['phone']
        raw_password = data['password']
        user_obj = None

        if not email and not phone:
           raise serializers.ValidationError("An email is required to login")

        # find users with with either a matching email or phone number
        user = User.objects.filter(       # Do this for phone OR email login
                Q(email=email) |
                Q(phone=phone)
            ).distinct()              

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("Invalid credentials")
        
        if user_obj:
            if user_obj.check_password(raw_password) == False:
                raise serializers.ValidationError("Invalid password")
        
        else:
            raise serializers.ValidationError("Invalid credentials")
                
        data['token'] = "SOME RANDOM TOKEN"
        return data
