# users/api/serializers.py

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField


####################
# USER SERIALIZERS #
####################

from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'phone',
        ]

        # prevents returning json from displaying given password
        extra_kwargs = {'password': {'write_only': True}}
    
    # overrides ModelSerializer.create() to save the object in the database after creation
    def create(self, validated_data):
        email      = validated_data['email'] 
        password   = validated_data['password']
        phone      = validated_data['phone']
        first_name = validated_data['first_name']
        last_name  = validated_data['last_name']

        # create the new user instance and save
        new_user = User(
                email = email,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
            )
        new_user.set_password(password)
        new_user.save()

        # create a profile for the user
        user_profile = Profile( 
                user_id = new_user
            )
        user_profile.save()

        return new_user


''' 
    UserLoginSerializer 
    User can login using a password, and either an email or phone number
'''
class UserLoginSerializer(serializers.ModelSerializer):
    email = EmailField(label='Email Address', allow_blank=True, required=False)
    phone = CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'phone',
            'password',
        ]

        # prevents returning json from displaying given password
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data['email']
        phone = data['phone']
        raw_password = data['password']
        user_object = None

        # if neither email nor phone number sent in request
        if not email and not phone:
            raise serializers.ValidationError("An email or phone is required to login")

        # find users with with either a matching email or phone number
        user = User.objects.filter(       
                Q(email=email) |
                Q(phone=phone)
            ).distinct()              

        # if 1 user is found, set user_object to that user
        if user.exists() and user.count() == 1:
            user_object = user.first()
        else:
            raise serializers.ValidationError("Invalid credentials")

        # if user_object exists
        if user_object:
            if user_object.check_password(raw_password) == False:
                raise serializers.ValidationError("Invalid password")

        # do this to return both user email AND phone number
        validated_data = data
        validated_data['id'] = user_object.id
        validated_data['email'] = user_object.email
        validated_data['phone'] = user_object.phone

        return validated_data


class UserUpdateSerializer(serializers.ModelSerializer): 
    email = EmailField(label='Email Address', required=True)
    phone = CharField(allow_blank=False, required=True)
    first_name = CharField(allow_blank=True, required=False)
    last_name = CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'phone',
            'first_name',
            'last_name',
        ]


    def validate(self, data):
        email = data['email']
        phone = data['phone']
        first_name = data['first_name']
        last_name = data['last_name']

        # if all fields are blank
        if not email or not phone or not first_name or not last_name:
            raise serializers.ValidationError("Email, phone, first_name, last_name required")
            
        return data


