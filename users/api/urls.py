from django.conf.urls import url
from django.urls import path, include

from .views import (
        UserCreate,
        UserLogin,
        UserUpdate,
    )

urlpatterns = [
    path('register', UserCreate.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('update', UserUpdate.as_view(), name='update-user'),
]
