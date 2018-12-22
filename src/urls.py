from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth', obtain_jwt_token, name='api-token-auth'),
    path('api/account/', include('accounts.api.urls'), name='accounts')
]
