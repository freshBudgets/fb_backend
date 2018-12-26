from django.conf.urls import url
from django.urls import path, include

from .views import (
        UserCreateAPIView,
        UserLoginAPIView,
        UserUpdateAPIView,
    )

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name='create'),
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('update', UserUpdateAPIView.as_view(), name='update'),
]
