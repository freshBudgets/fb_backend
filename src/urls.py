from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from .router import router


urlpatterns = [
    path('docs/', include_docs_urls(title="FreshBudgets API", 
            description="Documentation for endpoints", public=True,
            authentication_classes=[], permission_classes=[])),

    path('admin/', admin.site.urls),
    path('api/user/', include('users.api.urls'), name='user'),
    path('api/', include(router.urls)),
]
