# accounts/api/serializers.py

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_jwt(obj):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(obj)
    token = jwt_encode_handler(payload)
    return token


class UserCreateSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
            'token'
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

        new_user = User(
                email = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
            )
        new_user.set_password(password)
        new_user.save()

        validated_data['token'] = generate_jwt(new_user)

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
        user_object = None

        if not email and not phone:
           raise serializers.ValidationError("An email or phone is required to login")

        # find users with with either a matching email or phone number
        user = User.objects.filter(       
                Q(email=email) |
                Q(phone=phone)
            ).distinct()              

        # if there is 1 matching user
        if user.exists() and user.count() == 1:
            user_object = user.first()
        else:
            raise serializers.ValidationError("Invalid credentials")

        if user_object:
            if user_object.check_password(raw_password) == False:
                raise serializers.ValidationError("Invalid password")

        data['token'] = generate_jwt(user_object)
        return data



    
