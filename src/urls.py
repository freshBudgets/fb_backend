from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.api.urls'), name='user'),
    path('api/', include(router.urls)),
]
