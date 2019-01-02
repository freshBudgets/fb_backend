# users/api/views.py

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework import generics
from rest_framework.generics import (
        GenericAPIView,
        CreateAPIView,
    )
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


##################
# USER API VIEWS #
##################

from .serializers import (
        UserCreateSerializer,
        UserLoginSerializer,
        UserUpdateSerializer,
    )

from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreate(CreateAPIView):
    """
    Register and create user in database 
    """

    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            # TODO send out phone and/or email verification here

            return Response({'user info': serializer.data, 'tokens': generate_tokens(new_user)}, status=HTTP_201_CREATED)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


class UserLogin(GenericAPIView):
    """
    Login users with either a phone number or an email.
    """

    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            # get user from id in serializer. Generate JWT from found user
            current_user = User.objects.get(id=serializer.data['id'])
            return Response({'user info': serializer.data, 'tokens': generate_tokens(current_user)}, status=HTTP_200_OK)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)



class UserUpdate(GenericAPIView):
    """ 
    get:
    Get current user information to show on update page

    put:
    Update current user information
    """

    permission_classes = [IsAuthenticated]  
    serializer_class = UserUpdateSerializer

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_info = {}

        user_info['email'] = current_user.email
        user_info['phone'] = current_user.phone
        user_info['first_name'] = current_user.first_name
        user_info['last_name'] = current_user.last_name

        return Response({'user info': user_info}, HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdateSerializer(data=data)
        current_user = request.user

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.data
            updated_user = serializer.update(current_user, validated_data)

            # if email address updated
            if validated_data['email'] != current_user.email:
                # TODO Resend email validation ? 
                pass

            # if phone number updated
            if validated_data['phone'] != current_user.phone:
                # TODO resend phone verification
                pass

            return Response({'user info': validated_data, 'tokens': generate_tokens(current_user)}, status=HTTP_200_OK)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


# HELPER FUNCTION
# generates refresh and access JWT for a given user object
def generate_tokens(user):
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
    access_token = TokenObtainPairSerializer().get_token(user)
    refresh_token = AccessToken().for_user(user)

    return {'refresh token': str(access_token), 'access token': str(refresh_token)}
