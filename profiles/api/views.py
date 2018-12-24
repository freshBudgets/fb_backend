# profiles/api/views.py

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


#####################
# PROFILE API VIEWS #
#####################

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
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        # if data is not valid with serializer, raise exception
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.data
            return Response(validated_data, status=HTTP_200_OK)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]  
    # permission_classes = [AllowAny]
    serializer_class = UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = UserUpdateSerializer(data=data)

        current_user = request.user

        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.data

            if validated_data['email'] != current_user.email:
                # TODO Resend email validation ? 
                pass

            if validated_data['phone'] != current_user.phone:
                # TODO resend phone verification
                pass

            serializer.update(current_user, validated_data)
            # TODO return new token?
            return Response({'success': True, 'message': 'Updated user info'}, status=HTTP_200_OK)

        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)

