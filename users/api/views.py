# users/api/views.py

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.filters import (
        SearchFilter, 
        OrderingFilter
    )
from rest_framework.generics import (
        CreateAPIView,
        UpdateAPIView,
    )
from rest_framework.permissions import (
        AllowAny,
        IsAuthenticated,
    )


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


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()

            # TODO send out phone and/or email verification here

            return Response({'user info': serializer.data, 'tokens': generate_tokens(new_user)}, status=HTTP_200_OK)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            current_user = User.objects.get(id=serializer.data['id'])
            return Response({'user info': serializer.data, 'tokens': generate_tokens(current_user)}, status=HTTP_200_OK)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = UserUpdateSerializer

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

    
    # TODO update profile


# HELPER FUNCTION
# generates a refresh and access JWT for a given user object
def generate_tokens(user):
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
    tokenr = TokenObtainPairSerializer().get_token(user)
    tokena = AccessToken().for_user(user)

    return {'refresh token': str(tokenr), 'access token': str(tokena)}
