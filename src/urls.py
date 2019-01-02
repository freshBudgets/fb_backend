# src/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema view for docs 
schema_view = get_schema_view(
   openapi.Info(
      title="FreshBudgets API",
      default_version='v1',
      description="Documentation for API endpoints",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

from .router import router

urlpatterns = [
    # docs and admin site
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='FreshBudgets API',
                description="Documentation for Endpoints", public=True,
                authentication_classes=[], permission_classes=[])),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # non-viewset urls
    path('api/user/', include('users.api.urls'), name='user'),

    # viewset urls handled by the router
    path('api/', include(router.urls)),
]
